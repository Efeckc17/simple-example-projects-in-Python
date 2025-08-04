from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.utils import secure_filename
from PIL import Image
import uuid

from database import UserDatabase


app = Flask(__name__)
app.config['SECRET_KEY'] = 'plschange'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=24)

# Configure CORS for frontend communication
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5000", "http://127.0.0.1:5000", "file://"])

# Initialize database
db = UserDatabase()

# Upload configurations
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def resize_image(image_path, max_size=(300, 300)):
    """Resize uploaded image to maximum dimensions"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize maintaining aspect ratio
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(image_path, 'JPEG', quality=85)
            return True
    except Exception as e:
        print(f"Image resize error: {e}")
        return False


def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            # Decode JWT token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            
            # Get user from database
            current_user = db.get_user_by_id(current_user_id)
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated


def get_client_ip():
    """Get client IP address"""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']


@app.route('/api/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not all(k in data for k in ('username', 'email', 'password')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        # Basic validation
        if len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        if '@' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Create user
        result = db.create_user(username, email, password)
        
        if result['success']:
            # Log registration
            db.log_activity(result['user_id'], 'REGISTER', f'New user registered: {username}', get_client_ip())
            
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'user_id': result['user_id']
            }), 201
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        db.log_activity(None, 'ERROR', f'Registration error: {str(e)}', get_client_ip())
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('username', 'password')):
            return jsonify({'error': 'Missing username or password'}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # Authenticate user
        auth_result = db.authenticate_user(username, password)
        
        if auth_result['success']:
            user = auth_result['user']
            
            # Generate JWT token
            token_payload = {
                'user_id': user['id'],
                'username': user['username'],
                'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
            }
            
            token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
            
            # Log successful login
            db.log_activity(user['id'], 'LOGIN', f'User {username} logged in', get_client_ip())
            
            return jsonify({
                'success': True,
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'avatar_filename': user['avatar_filename']
                }
            }), 200
        else:
            # Log failed login attempt
            db.log_activity(None, 'LOGIN_FAILED', f'Failed login attempt for: {username}', get_client_ip())
            return jsonify({'error': auth_result['error']}), 401
            
    except Exception as e:
        db.log_activity(None, 'ERROR', f'Login error: {str(e)}', get_client_ip())
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get user profile information"""
    try:
        # Log profile access
        db.log_activity(current_user['id'], 'PROFILE_VIEW', 'User viewed profile', get_client_ip())
        
        return jsonify({
            'success': True,
            'user': current_user
        }), 200
        
    except Exception as e:
        db.log_activity(current_user['id'], 'ERROR', f'Profile view error: {str(e)}', get_client_ip())
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update user profile information"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip() if data.get('username') else None
        email = data.get('email', '').strip().lower() if data.get('email') else None
        
        # Validate input
        if username and len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        
        if email and '@' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Update profile
        result = db.update_user_profile(current_user['id'], username, email)
        
        if result['success']:
            # Log profile update
            changes = []
            if username:
                changes.append(f'username to {username}')
            if email:
                changes.append(f'email to {email}')
            
            db.log_activity(current_user['id'], 'PROFILE_UPDATE', 
                          f'User updated: {", ".join(changes)}', get_client_ip())
            
            # Get updated user info
            updated_user = db.get_user_by_id(current_user['id'])
            
            return jsonify({
                'success': True,
                'message': result['message'],
                'user': updated_user
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        db.log_activity(current_user['id'], 'ERROR', f'Profile update error: {str(e)}', get_client_ip())
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/upload-avatar', methods=['POST'])
@token_required
def upload_avatar(current_user):
    """Upload user avatar image"""
    try:
        if 'avatar' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['avatar']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG, GIF allowed'}), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large. Maximum 5MB allowed'}), 400
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{current_user['id']}_{uuid.uuid4().hex[:8]}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Resize image
        if not resize_image(file_path):
            os.remove(file_path)
            return jsonify({'error': 'Failed to process image'}), 500
        
        # Update user avatar in database
        result = db.update_user_profile(current_user['id'], avatar_filename=unique_filename)
        
        if result['success']:
            # Log avatar upload
            db.log_activity(current_user['id'], 'AVATAR_UPLOAD', 
                          f'User uploaded new avatar: {unique_filename}', get_client_ip())
            
            return jsonify({
                'success': True,
                'message': 'Avatar uploaded successfully',
                'avatar_filename': unique_filename
            }), 200
        else:
            # Remove uploaded file if database update failed
            os.remove(file_path)
            return jsonify({'error': 'Failed to update avatar'}), 500
            
    except Exception as e:
        db.log_activity(current_user['id'], 'ERROR', f'Avatar upload error: {str(e)}', get_client_ip())
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/avatar/<filename>')
def get_avatar(filename):
    """Serve avatar images"""
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception:
        # Return default avatar or 404
        return jsonify({'error': 'Avatar not found'}), 404


@app.route('/api/logs', methods=['GET'])
@token_required
def get_logs(current_user):
    """Get server logs (admin functionality)"""
    try:
        # Get limit from query parameters
        limit = request.args.get('limit', 50, type=int)
        limit = min(limit, 200)  # Maximum 200 logs
        
        # Get logs from database
        logs = db.get_server_logs(limit)
        
        # Log access to logs
        db.log_activity(current_user['id'], 'LOGS_VIEW', 
                      f'User viewed {len(logs)} server logs', get_client_ip())
        
        return jsonify({
            'success': True,
            'logs': logs,
            'total': len(logs)
        }), 200
        
    except Exception as e:
        db.log_activity(current_user['id'], 'ERROR', f'Logs view error: {str(e)}', get_client_ip())
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    """Get user statistics"""
    try:
        stats = db.get_user_stats()
        
        # Log stats access
        db.log_activity(current_user['id'], 'STATS_VIEW', 'User viewed statistics', get_client_ip())
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        db.log_activity(current_user['id'], 'ERROR', f'Stats view error: {str(e)}', get_client_ip())
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/validate-token', methods=['GET'])
@token_required
def validate_token(current_user):
    """Validate JWT token"""
    return jsonify({
        'success': True,
        'message': 'Token is valid',
        'user': current_user
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'User Management API',
        'timestamp': datetime.now().isoformat()
    }), 200


# Frontend Routes
@app.route('/')
def serve_frontend():
    """Serve the main frontend page"""
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')
    return send_from_directory(frontend_dir, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static frontend files (CSS, JS, etc.)"""
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')
    return send_from_directory(frontend_dir, filename)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 Starting User Management API...")
    print("📡 Server: http://localhost:5000")
    print("📚 API Endpoints:")
    print("   POST /api/register - User registration")
    print("   POST /api/login - User login")
    print("   GET  /api/profile - Get user profile")
    print("   PUT  /api/profile - Update user profile")
    print("   POST /api/upload-avatar - Upload profile picture")
    print("   GET  /api/logs - Get server logs")
    print("   GET  /api/stats - Get user statistics")
    print("   GET  /api/health - Health check")
    print("⏹️  Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)