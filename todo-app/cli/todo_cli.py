import sys
import os

# Add parent directory to path to import database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import TodoDatabase


class TodoCLI:
    
    def __init__(self):
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "todo_cli.db")
        
        # Initialize database connection
        self.db = TodoDatabase(db_path)
        print("📝 TODO CLI Application")
        print(f"💾 SQLite Database: {db_path}")
    
    def print_banner(self):
        """Print application banner"""
        print("\n" + "=" * 50)
        print("📝  TODO CLI APPLICATION  📝")
        print("💾  SQLite Database Learning Project")
        print("=" * 50)
    
    def show_main_menu(self):
        """Display main menu options"""
        print("\n📋 MAIN MENU")
        print("-" * 30)
        print("1. 📝 Add Task")
        print("2. 📋 View All Tasks")
        print("3. ✅ View Completed Tasks")
        print("4. ⏳ View Pending Tasks")
        print("5. 📝 Update Task")
        print("6. ✅ Mark Complete/Incomplete")
        print("7. 🗑️  Delete Task")
        print("8. 🔍 Search Tasks")
        print("9. 📊 Show Statistics")
        print("10. 🗑️ Clear Completed Tasks")
        print("11. 💾 Database Info")
        print("12. ❓ Help")
        print("0. 🚪 Exit")
        print("-" * 30)
    
    def add_task(self):
        """Add a new task"""
        print("\n📝 ADD NEW TASK")
        print("-" * 20)
        
        task = input("📌 Task title: ").strip()
        if not task:
            print("❌ Task title cannot be empty!")
            return
        
        description = input("📄 Description (optional): ").strip()
        
        print("\n🎯 Priority levels:")
        print("  1. Low")
        print("  2. Medium (default)")
        print("  3. High")
        
        priority_choice = input("Priority (1-3): ").strip()
        priority_map = {"1": "low", "2": "medium", "3": "high"}
        priority = priority_map.get(priority_choice, "medium")
        
        if self.db.add_task(task, description, priority):
            print(f"✅ Task '{task}' added successfully!")
        else:
            print("❌ Failed to add task!")
    
    def view_tasks(self, filter_type="all"):
        """View tasks with different filters"""
        if filter_type == "all":
            tasks = self.db.get_all_tasks()
            title = "📋 ALL TASKS"
        elif filter_type == "completed":
            tasks = self.db.get_tasks_by_status(True)
            title = "✅ COMPLETED TASKS"
        elif filter_type == "pending":
            tasks = self.db.get_tasks_by_status(False)
            title = "⏳ PENDING TASKS"
        
        print(f"\n{title}")
        print("-" * len(title))
        
        if not tasks:
            print("📭 No tasks found!")
            return
        
        for task in tasks:
            task_id, title, desc, completed, priority, created, completed_date = task
            
            # Status icon
            status_icon = "✅" if completed else "⏳"
            
            # Priority color coding
            priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            priority_icon = priority_icons.get(priority, "⚪")
            
            print(f"\n{status_icon} [{task_id}] {title}")
            print(f"    {priority_icon} Priority: {priority.upper()}")
            
            if desc:
                print(f"    📄 {desc}")
            
            print(f"    📅 Created: {created}")
            
            if completed and completed_date:
                print(f"    ✅ Completed: {completed_date}")
    
    def update_task(self):
        """Update an existing task"""
        print("\n📝 UPDATE TASK")
        print("-" * 15)
        
        try:
            task_id = int(input("🆔 Enter task ID to update: "))
        except ValueError:
            print("❌ Invalid task ID!")
            return
        
        # Get current task info
        tasks = self.db.get_all_tasks()
        current_task = None
        for task in tasks:
            if task[0] == task_id:
                current_task = task
                break
        
        if not current_task:
            print(f"❌ Task with ID {task_id} not found!")
            return
        
        print(f"\nCurrent task: {current_task[1]}")
        print("Leave empty to keep current value")
        
        # Get new values
        new_task = input(f"📌 New title [{current_task[1]}]: ").strip()
        new_desc = input(f"📄 New description [{current_task[2] or 'None'}]: ").strip()
        
        print("\n🎯 Priority: 1=Low, 2=Medium, 3=High")
        new_priority_input = input(f"Priority [{current_task[4]}]: ").strip()
        
        priority_map = {"1": "low", "2": "medium", "3": "high"}
        new_priority = priority_map.get(new_priority_input, None)
        
        # Update only changed fields
        updates = {}
        if new_task:
            updates['task'] = new_task
        if new_desc:
            updates['description'] = new_desc
        if new_priority:
            updates['priority'] = new_priority
        
        if not updates:
            print("⚠️ No changes made!")
            return
        
        if self.db.update_task(task_id, **updates):
            print("✅ Task updated successfully!")
        else:
            print("❌ Failed to update task!")
    
    def toggle_completion(self):
        """Mark task as complete or incomplete"""
        print("\n✅ TOGGLE TASK COMPLETION")
        print("-" * 25)
        
        try:
            task_id = int(input("🆔 Enter task ID: "))
        except ValueError:
            print("❌ Invalid task ID!")
            return
        
        # Get current status
        tasks = self.db.get_all_tasks()
        current_task = None
        for task in tasks:
            if task[0] == task_id:
                current_task = task
                break
        
        if not current_task:
            print(f"❌ Task with ID {task_id} not found!")
            return
        
        current_status = current_task[3]
        new_status = not current_status
        
        if self.db.mark_completed(task_id, new_status):
            action = "completed" if new_status else "pending"
            print(f"✅ Task marked as {action}!")
        else:
            print("❌ Failed to update task status!")
    
    def delete_task(self):
        """Delete a task"""
        print("\n🗑️ DELETE TASK")
        print("-" * 15)
        
        try:
            task_id = int(input("🆔 Enter task ID to delete: "))
        except ValueError:
            print("❌ Invalid task ID!")
            return
        
        # Confirm deletion
        confirm = input(f"⚠️ Are you sure you want to delete task {task_id}? (y/N): ").lower()
        
        if confirm == 'y':
            if self.db.delete_task(task_id):
                print("✅ Task deleted successfully!")
            else:
                print("❌ Failed to delete task!")
        else:
            print("❌ Deletion cancelled!")
    
    def search_tasks(self):
        """Search for tasks"""
        print("\n🔍 SEARCH TASKS")
        print("-" * 15)
        
        search_term = input("🔍 Enter search term: ").strip()
        
        if not search_term:
            print("❌ Search term cannot be empty!")
            return
        
        tasks = self.db.search_tasks(search_term)
        
        if not tasks:
            print(f"📭 No tasks found containing '{search_term}'")
            return
        
        print(f"\n🔍 SEARCH RESULTS FOR '{search_term}'")
        print("-" * 30)
        
        for task in tasks:
            task_id, title, desc, completed, priority, created, completed_date = task
            status_icon = "✅" if completed else "⏳"
            priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            priority_icon = priority_icons.get(priority, "⚪")
            
            print(f"\n{status_icon} [{task_id}] {title}")
            print(f"    {priority_icon} Priority: {priority.upper()}")
            if desc:
                print(f"    📄 {desc}")
    
    def show_statistics(self):
        """Display task statistics"""
        print("\n📊 TASK STATISTICS")
        print("-" * 20)
        
        stats = self.db.get_task_stats()
        
        if not stats:
            print("❌ Unable to retrieve statistics!")
            return
        
        print(f"📋 Total tasks: {stats['total']}")
        print(f"✅ Completed: {stats['completed']}")
        print(f"⏳ Pending: {stats['pending']}")
        print(f"📈 Completion rate: {stats['completion_rate']:.1f}%")
        
        if stats['priority_counts']:
            print("\n🎯 Pending tasks by priority:")
            for priority, count in stats['priority_counts'].items():
                priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                icon = priority_icons.get(priority, "⚪")
                print(f"    {icon} {priority.capitalize()}: {count}")
    
    def clear_completed(self):
        """Clear all completed tasks"""
        print("\n🗑️ CLEAR COMPLETED TASKS")
        print("-" * 25)
        
        # Get completed task count
        completed_tasks = self.db.get_tasks_by_status(True)
        count = len(completed_tasks)
        
        if count == 0:
            print("📭 No completed tasks to clear!")
            return
        
        print(f"Found {count} completed task(s)")
        confirm = input("⚠️ Are you sure you want to delete all completed tasks? (y/N): ").lower()
        
        if confirm == 'y':
            deleted = self.db.clear_completed_tasks()
            print(f"✅ Deleted {deleted} completed tasks!")
        else:
            print("❌ Operation cancelled!")
    
    def show_database_info(self):
        """Show database information"""
        print("\n💾 DATABASE INFORMATION")
        print("-" * 25)
        
        info = self.db.get_database_info()
        
        if not info:
            print("❌ Unable to retrieve database info!")
            return
        
        print(f"📁 Database file: {info['database_path']}")
        print(f"📦 File size: {info['file_size_kb']} KB")
        print(f"📊 Table columns: {info['columns']}")
        
        print("\n🏗️ Table structure:")
        for col in info['column_info']:
            print(f"    • {col[1]} ({col[2]})")
    
    def show_help(self):
        """Show help information"""
        print("\n❓ HELP - SQL OPERATIONS EXPLAINED")
        print("-" * 40)
        print("This TODO app demonstrates basic SQL operations:")
        print()
        print("📝 CREATE (INSERT):")
        print("   • Adding new tasks to database")
        print("   • SQL: INSERT INTO todos (task, description, priority) VALUES (?, ?, ?)")
        print()
        print("📋 READ (SELECT):")
        print("   • Viewing all tasks, filtering by status")
        print("   • SQL: SELECT * FROM todos WHERE completed = ?")
        print()
        print("📝 UPDATE:")
        print("   • Modifying existing tasks")
        print("   • SQL: UPDATE todos SET task = ? WHERE id = ?")
        print()
        print("🗑️ DELETE:")
        print("   • Removing tasks from database")
        print("   • SQL: DELETE FROM todos WHERE id = ?")
        print()
        print("🔍 SEARCH:")
        print("   • Finding tasks with LIKE operator")
        print("   • SQL: SELECT * FROM todos WHERE task LIKE '%search%'")
        print()
        print("📊 AGGREGATION:")
        print("   • COUNT(), GROUP BY for statistics")
        print("   • SQL: SELECT COUNT(*) FROM todos WHERE completed = 1")
    
    def run(self):
        """Main application loop"""
        try:
            self.print_banner()
            
            while True:
                self.show_main_menu()
                
                choice = input("\nSelect option (0-12): ").strip()
                
                if choice == "0":
                    print("\n👋 Thank you for using TODO CLI!")
                    print("💾 All data saved to SQLite database")
                    break
                
                elif choice == "1":
                    self.add_task()
                
                elif choice == "2":
                    self.view_tasks("all")
                
                elif choice == "3":
                    self.view_tasks("completed")
                
                elif choice == "4":
                    self.view_tasks("pending")
                
                elif choice == "5":
                    self.update_task()
                
                elif choice == "6":
                    self.toggle_completion()
                
                elif choice == "7":
                    self.delete_task()
                
                elif choice == "8":
                    self.search_tasks()
                
                elif choice == "9":
                    self.show_statistics()
                
                elif choice == "10":
                    self.clear_completed()
                
                elif choice == "11":
                    self.show_database_info()
                
                elif choice == "12":
                    self.show_help()
                
                else:
                    print("❌ Invalid choice! Please select 0-12.")
                
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Application interrupted. Goodbye!")
        
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please restart the application.")


def main():
    """Main function"""
    app = TodoCLI()
    app.run()


if __name__ == "__main__":
    main()