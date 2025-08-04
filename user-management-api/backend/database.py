import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict, List
import bcrypt


class UserDatabase:
    
    def __init__(self, db_path: str = "users.db"):
        # Store database path relative to backend directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(script_dir, db_path)
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    avatar_filename TEXT DEFAULT 'default-avatar.png',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            # Logs table for server activity
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS server_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    ip_address TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # User sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    token TEXT UNIQUE NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    expires_at TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            conn.commit()
            conn.close()
            
            print(f"✅ Database initialized: {self.db_path}")
            
        except sqlite3.Error as e:
            print(f"❌ Database initialization error: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    
    def create_user(self, username: str, email: str, password: str) -> Dict:
        """Create a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                conn.close()
                return {"success": False, "error": "Username or email already exists"}
            
            # Hash password
            password_hash = self.hash_password(password)
            
            # Insert user
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (username, email, password_hash, datetime.now().isoformat(), datetime.now().isoformat()))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {"success": True, "user_id": user_id, "message": "User created successfully"}
            
        except sqlite3.Error as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    def authenticate_user(self, username: str, password: str) -> Dict:
        """Authenticate user credentials"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get user by username or email
            cursor.execute("""
                SELECT id, username, email, password_hash, avatar_filename, is_active
                FROM users 
                WHERE (username = ? OR email = ?) AND is_active = 1
            """, (username, username))
            
            user = cursor.fetchone()
            conn.close()
            
            if not user:
                return {"success": False, "error": "User not found"}
            
            user_id, username, email, password_hash, avatar_filename, is_active = user
            
            # Verify password
            if not self.verify_password(password, password_hash):
                return {"success": False, "error": "Invalid password"}
            
            return {
                "success": True,
                "user": {
                    "id": user_id,
                    "username": username,
                    "email": email,
                    "avatar_filename": avatar_filename
                }
            }
            
        except sqlite3.Error as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user information by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, email, avatar_filename, created_at, updated_at
                FROM users 
                WHERE id = ? AND is_active = 1
            """, (user_id,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "avatar_filename": user[3],
                    "created_at": user[4],
                    "updated_at": user[5]
                }
            return None
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def update_user_profile(self, user_id: int, username: str = None, 
                          email: str = None, avatar_filename: str = None) -> Dict:
        """Update user profile information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build dynamic update query
            updates = []
            params = []
            
            if username:
                # Check if username is already taken by another user
                cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (username, user_id))
                if cursor.fetchone():
                    conn.close()
                    return {"success": False, "error": "Username already exists"}
                updates.append("username = ?")
                params.append(username)
            
            if email:
                # Check if email is already taken by another user
                cursor.execute("SELECT id FROM users WHERE email = ? AND id != ?", (email, user_id))
                if cursor.fetchone():
                    conn.close()
                    return {"success": False, "error": "Email already exists"}
                updates.append("email = ?")
                params.append(email)
            
            if avatar_filename:
                updates.append("avatar_filename = ?")
                params.append(avatar_filename)
            
            if not updates:
                conn.close()
                return {"success": False, "error": "No updates provided"}
            
            # Add updated_at timestamp
            updates.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            params.append(user_id)
            
            # Execute update
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                return {"success": True, "message": "Profile updated successfully"}
            else:
                conn.close()
                return {"success": False, "error": "User not found"}
                
        except sqlite3.Error as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    def log_activity(self, user_id: Optional[int], action: str, 
                    details: str = "", ip_address: str = "") -> bool:
        """Log server activity"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO server_logs (user_id, action, details, ip_address, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, action, details, ip_address, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Logging error: {e}")
            return False
    
    def get_server_logs(self, limit: int = 100) -> List[Dict]:
        """Get server logs with user information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    sl.id, sl.user_id, u.username, sl.action, 
                    sl.details, sl.ip_address, sl.timestamp
                FROM server_logs sl
                LEFT JOIN users u ON sl.user_id = u.id
                ORDER BY sl.timestamp DESC
                LIMIT ?
            """, (limit,))
            
            logs = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "id": log[0],
                    "user_id": log[1],
                    "username": log[2] or "System",
                    "action": log[3],
                    "details": log[4],
                    "ip_address": log[5],
                    "timestamp": log[6]
                }
                for log in logs
            ]
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def get_user_stats(self) -> Dict:
        """Get user statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total users
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
            total_users = cursor.fetchone()[0]
            
            # Users registered today
            today = datetime.now().date().isoformat()
            cursor.execute("SELECT COUNT(*) FROM users WHERE DATE(created_at) = ? AND is_active = 1", (today,))
            today_users = cursor.fetchone()[0]
            
            # Total logs
            cursor.execute("SELECT COUNT(*) FROM server_logs")
            total_logs = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total_users": total_users,
                "today_users": today_users,
                "total_logs": total_logs
            }
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {"total_users": 0, "today_users": 0, "total_logs": 0}


def demo_database():
    """Demonstrate database functionality"""
    print("👤 User Database Demo")
    print("=" * 30)
    
    db = UserDatabase("demo_users.db")
    
    # Create test user
    result = db.create_user("testuser", "test@example.com", "password123")
    print(f"Create user: {result}")
    
    # Authenticate user
    auth_result = db.authenticate_user("testuser", "password123")
    print(f"Authenticate: {auth_result}")
    
    # Log activity
    if auth_result["success"]:
        user_id = auth_result["user"]["id"]
        db.log_activity(user_id, "LOGIN", "User logged in", "127.0.0.1")
        
        # Update profile
        update_result = db.update_user_profile(user_id, email="newemail@example.com")
        print(f"Update profile: {update_result}")
        
        # Get logs
        logs = db.get_server_logs(5)
        print(f"Recent logs: {len(logs)} entries")
        for log in logs:
            print(f"  {log['timestamp']}: {log['username']} - {log['action']}")


if __name__ == "__main__":
    demo_database()