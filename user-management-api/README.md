# 👤 User Management API

A full-stack web application demonstrating modern API development with Python Flask backend and vanilla JavaScript frontend.

## 🚀 Features

### 🔐 Authentication System
- **User Registration** - Create new accounts with validation
- **JWT Login** - Secure token-based authentication
- **Password Hashing** - bcrypt encryption for security
- **Token Validation** - Automatic session management

### 👤 Profile Management
- **View Profile** - Display user information
- **Edit Username** - Update username with validation
- **Edit Email** - Change email address
- **Avatar Upload** - Profile picture with image processing
- **Real-time Updates** - Live UI updates after changes

### 📊 Admin Dashboard
- **User Statistics** - Total users, daily registrations
- **Server Logs** - Activity monitoring with filtering
- **Real-time Data** - Auto-refreshing dashboard
- **Log Management** - Categorized activity tracking

### 🛠️ Technical Features
- **RESTful API** - Clean endpoint design
- **SQLite Database** - Portable database solution
- **Image Processing** - Avatar resizing and optimization
- **CORS Support** - Cross-origin resource sharing
- **Error Handling** - Comprehensive error management
- **Input Validation** - Both frontend and backend validation

## 📁 Project Structure

```
user-management-api/
├── backend/
│   ├── app.py              # Flask API server
│   ├── database.py         # Database operations
│   └── users.db           # SQLite database (auto-created)
├── frontend/
│   ├── index.html         # Main HTML page
│   ├── style.css          # Modern CSS styling
│   └── script.js          # JavaScript API client
├── uploads/               # User avatar storage
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠️ Installation & Setup

### 1. Install Dependencies
```bash
cd user-management-api
pip install -r requirements.txt
```

### 2. Start Backend Server
```bash
cd backend
python app.py
```
Server will start at: http://localhost:5000

### 3. Open Frontend
```bash
cd frontend
# Option 1: Simple HTTP server
python -m http.server 3000

# Option 2: Open directly in browser
open index.html  # macOS
start index.html  # Windows
```
Frontend will be available at: http://localhost:3000

## 📡 API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/validate-token` - Token validation

### Profile Management
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile
- `POST /api/upload-avatar` - Upload avatar
- `GET /api/avatar/<filename>` - Serve avatar images

### Admin Functions
- `GET /api/logs` - Get server logs
- `GET /api/stats` - Get user statistics
- `GET /api/health` - API health check

## 🎯 API Usage Examples

### Register a New User
```javascript
const response = await fetch('http://localhost:5000/api/register', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: 'johndoe',
        email: 'john@example.com',
        password: 'securepassword'
    })
});

const data = await response.json();
```

### Login and Get Token
```javascript
const response = await fetch('http://localhost:5000/api/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: 'johndoe',
        password: 'securepassword'
    })
});

const data = await response.json();
const token = data.token; // Use for authenticated requests
```

### Get User Profile
```javascript
const response = await fetch('http://localhost:5000/api/profile', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
});

const data = await response.json();
```

### Upload Avatar
```javascript
const formData = new FormData();
formData.append('avatar', fileInput.files[0]);

const response = await fetch('http://localhost:5000/api/upload-avatar', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`
    },
    body: formData
});
```

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    avatar_filename TEXT DEFAULT 'default-avatar.png',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

### Server Logs Table
```sql
CREATE TABLE server_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    details TEXT,
    ip_address TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## 🎨 Frontend Features

### Modern UI/UX
- **Responsive Design** - Works on all devices
- **Gradient Backgrounds** - Beautiful visual design
- **Smooth Animations** - Enhanced user experience
- **Modal Dialogs** - Inline editing functionality
- **Real-time Alerts** - User feedback system

### JavaScript Features
- **Fetch API** - Modern HTTP requests
- **LocalStorage** - Token persistence
- **Event Delegation** - Efficient event handling
- **Form Validation** - Client-side validation
- **File Upload** - Drag & drop avatar upload

## 🔒 Security Features

### Backend Security
- **Password Hashing** - bcrypt with salt
- **JWT Tokens** - Secure authentication
- **Input Validation** - SQL injection prevention
- **File Validation** - Image upload security
- **CORS Configuration** - Cross-origin protection

### Frontend Security
- **Token Management** - Secure storage
- **Input Sanitization** - XSS prevention
- **File Type Validation** - Upload security
- **Error Handling** - No sensitive data exposure

## 🧪 Testing the API

### 1. Test with cURL
```bash
# Register
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# Get Profile (replace TOKEN with actual token)
curl -X GET http://localhost:5000/api/profile \
  -H "Authorization: Bearer TOKEN"
```

### 2. Test with Python
```python
import requests

# Register
response = requests.post('http://localhost:5000/api/register', json={
    'username': 'pythonuser',
    'email': 'python@example.com',
    'password': 'python123'
})
print(response.json())

# Login
response = requests.post('http://localhost:5000/api/login', json={
    'username': 'pythonuser',
    'password': 'python123'
})
token = response.json()['token']

# Get Profile
response = requests.get('http://localhost:5000/api/profile', 
                       headers={'Authorization': f'Bearer {token}'})
print(response.json())
```

## 🎓 Learning Objectives

This project teaches:

### Backend Development
- **Flask Framework** - Web application development
- **RESTful API Design** - HTTP methods and status codes
- **Database Integration** - SQLite with Python
- **Authentication** - JWT and password security
- **File Handling** - Image upload and processing
- **Error Handling** - Exception management

### Frontend Development
- **Modern JavaScript** - ES6+ features
- **Fetch API** - Asynchronous HTTP requests
- **DOM Manipulation** - Dynamic UI updates
- **Event Handling** - User interaction management
- **Form Validation** - Client-side validation
- **Responsive Design** - Mobile-first CSS

### Full-Stack Integration
- **API Communication** - Frontend-backend data flow
- **Authentication Flow** - Token-based security
- **State Management** - User session handling
- **Error Propagation** - End-to-end error handling

## 🚀 Deployment Notes

### Production Considerations
1. **Change Secret Key** - Use environment variables
2. **Database Migration** - Consider PostgreSQL for production
3. **File Storage** - Use cloud storage (AWS S3, etc.)
4. **HTTPS** - Enable SSL/TLS encryption
5. **Rate Limiting** - Prevent abuse
6. **Logging** - Structured logging for monitoring

### Environment Variables
```bash
export SECRET_KEY="your-production-secret-key"
export DATABASE_URL="sqlite:///production.db"
export UPLOAD_FOLDER="/path/to/uploads"
```

## 🐛 Troubleshooting

### Common Issues
1. **CORS Errors** - Check frontend URL in CORS configuration
2. **Token Errors** - Verify JWT secret key consistency
3. **File Upload Fails** - Check upload directory permissions
4. **Database Errors** - Ensure SQLite file is writable

### Debug Mode
Set Flask debug mode for development:
```python
app.run(debug=True)
```

## 📄 License

MIT License - Feel free to use this project for learning and development!

---

🎯 **Perfect for learning modern web development with Python and JavaScript!**