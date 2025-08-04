import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional


class TodoDatabase:
    
    def __init__(self, db_path: str = "todo.db"):
        # Store database file path
        self.db_path = db_path
        # Initialize database and create table if not exists
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        try:
            # Connect to SQLite database (creates file if doesn't exist)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create todos table with all necessary columns
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT 0,
                    priority TEXT DEFAULT 'medium',
                    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    completed_date TEXT
                )
            """)
            
            # Save changes and close connection
            conn.commit()
            conn.close()
            
            print(f"📁 Database initialized: {self.db_path}")
            
        except sqlite3.Error as e:
            print(f"❌ Database initialization error: {e}")
    
    def add_task(self, task: str, description: str = "", priority: str = "medium") -> bool:
        """Add a new task to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert new task with current timestamp
            cursor.execute("""
                INSERT INTO todos (task, description, priority, created_date)
                VALUES (?, ?, ?, ?)
            """, (task, description, priority, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Task added: {task}")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error adding task: {e}")
            return False
    
    def get_all_tasks(self) -> List[Tuple]:
        """Retrieve all tasks from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Select all tasks ordered by creation date
            cursor.execute("""
                SELECT id, task, description, completed, priority, created_date, completed_date
                FROM todos
                ORDER BY created_date DESC
            """)
            
            tasks = cursor.fetchall()
            conn.close()
            
            return tasks
            
        except sqlite3.Error as e:
            print(f"❌ Error retrieving tasks: {e}")
            return []
    
    def get_tasks_by_status(self, completed: bool) -> List[Tuple]:
        """Get tasks filtered by completion status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, task, description, completed, priority, created_date, completed_date
                FROM todos
                WHERE completed = ?
                ORDER BY created_date DESC
            """, (completed,))
            
            tasks = cursor.fetchall()
            conn.close()
            
            return tasks
            
        except sqlite3.Error as e:
            print(f"❌ Error retrieving tasks by status: {e}")
            return []
    
    def update_task(self, task_id: int, task: str = None, description: str = None, 
                   priority: str = None) -> bool:
        """Update an existing task"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build dynamic UPDATE query based on provided parameters
            updates = []
            params = []
            
            if task is not None:
                updates.append("task = ?")
                params.append(task)
            
            if description is not None:
                updates.append("description = ?")
                params.append(description)
            
            if priority is not None:
                updates.append("priority = ?")
                params.append(priority)
            
            if not updates:
                return False
            
            # Add task_id to parameters
            params.append(task_id)
            
            # Execute update query
            query = f"UPDATE todos SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                print(f"📝 Task {task_id} updated successfully")
                return True
            else:
                conn.close()
                print(f"❌ Task {task_id} not found")
                return False
                
        except sqlite3.Error as e:
            print(f"❌ Error updating task: {e}")
            return False
    
    def mark_completed(self, task_id: int, completed: bool = True) -> bool:
        """Mark a task as completed or incomplete"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Set completion status and date
            completed_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if completed else None
            
            cursor.execute("""
                UPDATE todos 
                SET completed = ?, completed_date = ?
                WHERE id = ?
            """, (completed, completed_date, task_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                status = "completed" if completed else "incomplete"
                print(f"✅ Task {task_id} marked as {status}")
                return True
            else:
                conn.close()
                print(f"❌ Task {task_id} not found")
                return False
                
        except sqlite3.Error as e:
            print(f"❌ Error updating task status: {e}")
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM todos WHERE id = ?", (task_id,))
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                print(f"🗑️ Task {task_id} deleted")
                return True
            else:
                conn.close()
                print(f"❌ Task {task_id} not found")
                return False
                
        except sqlite3.Error as e:
            print(f"❌ Error deleting task: {e}")
            return False
    
    def search_tasks(self, search_term: str) -> List[Tuple]:
        """Search tasks by task name or description"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Search in both task and description fields
            cursor.execute("""
                SELECT id, task, description, completed, priority, created_date, completed_date
                FROM todos
                WHERE task LIKE ? OR description LIKE ?
                ORDER BY created_date DESC
            """, (f"%{search_term}%", f"%{search_term}%"))
            
            tasks = cursor.fetchall()
            conn.close()
            
            return tasks
            
        except sqlite3.Error as e:
            print(f"❌ Error searching tasks: {e}")
            return []
    
    def get_task_stats(self) -> dict:
        """Get statistics about tasks"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count total tasks
            cursor.execute("SELECT COUNT(*) FROM todos")
            total = cursor.fetchone()[0]
            
            # Count completed tasks
            cursor.execute("SELECT COUNT(*) FROM todos WHERE completed = 1")
            completed = cursor.fetchone()[0]
            
            # Count by priority
            cursor.execute("""
                SELECT priority, COUNT(*) 
                FROM todos 
                WHERE completed = 0 
                GROUP BY priority
            """)
            priority_counts = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                'total': total,
                'completed': completed,
                'pending': total - completed,
                'completion_rate': (completed / total * 100) if total > 0 else 0,
                'priority_counts': priority_counts
            }
            
        except sqlite3.Error as e:
            print(f"❌ Error getting statistics: {e}")
            return {}
    
    def clear_completed_tasks(self) -> int:
        """Delete all completed tasks"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM todos WHERE completed = 1")
            deleted_count = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            print(f"🗑️ Deleted {deleted_count} completed tasks")
            return deleted_count
            
        except sqlite3.Error as e:
            print(f"❌ Error clearing completed tasks: {e}")
            return 0
    
    def get_database_info(self) -> dict:
        """Get information about the database"""
        try:
            # File size
            file_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Table info
            cursor.execute("PRAGMA table_info(todos)")
            columns = cursor.fetchall()
            
            conn.close()
            
            return {
                'database_path': self.db_path,
                'file_size_bytes': file_size,
                'file_size_kb': round(file_size / 1024, 2),
                'columns': len(columns),
                'column_info': columns
            }
            
        except sqlite3.Error as e:
            print(f"❌ Error getting database info: {e}")
            return {}


def demo_database_usage():
    """Demonstrate basic database operations"""
    print("🎯 SQLite Database Demo")
    print("=" * 40)
    
    # Initialize database
    db = TodoDatabase("demo_todo.db")
    
    # Add some sample tasks
    print("\n📝 Adding sample tasks...")
    db.add_task("Learn Python", "Study Python basics and advanced concepts", "high")
    db.add_task("Build TODO app", "Create CLI and GUI versions", "medium")
    db.add_task("Study SQLite", "Learn database operations", "high")
    db.add_task("Buy groceries", "Milk, bread, eggs", "low")
    
    # Show all tasks
    print("\n📋 All tasks:")
    tasks = db.get_all_tasks()
    for task in tasks:
        status = "✅" if task[3] else "⏳"
        print(f"{status} [{task[0]}] {task[1]} ({task[4]} priority)")
    
    # Mark some tasks as completed
    print("\n✅ Marking tasks as completed...")
    db.mark_completed(1, True)
    db.mark_completed(3, True)
    
    # Show statistics
    print("\n📊 Statistics:")
    stats = db.get_task_stats()
    print(f"Total tasks: {stats['total']}")
    print(f"Completed: {stats['completed']}")
    print(f"Pending: {stats['pending']}")
    print(f"Completion rate: {stats['completion_rate']:.1f}%")
    
    # Search tasks
    print("\n🔍 Searching for 'Python':")
    results = db.search_tasks("Python")
    for task in results:
        print(f"  • {task[1]}")
    
    print("\n🎉 Demo completed!")


if __name__ == "__main__":
    demo_database_usage()