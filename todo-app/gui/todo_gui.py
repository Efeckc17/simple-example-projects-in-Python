import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os

# Add parent directory to path to import database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import TodoDatabase


class TodoGUI:
    
    def __init__(self):
        # Create main window
        self.window = tk.Tk()
        self.setup_window()
        
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "todo_gui.db")
        
        # Initialize database
        self.db = TodoDatabase(db_path)
        
        # Track current filter
        self.current_filter = "all"
        
        # Create GUI components
        self.create_widgets()
        
        # Load initial data
        self.refresh_task_list()
    
    def setup_window(self):
        self.window.title("📝 TODO App - SQLite Database")
        self.window.resizable(True, True)
        self.window.minsize(800, 600)
        
        # Apply modern theme
        style = ttk.Style()
        style.theme_use('clam')
    
    def create_widgets(self):
        # Configure main window grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # Main container
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.create_header(main_frame)
        self.create_toolbar(main_frame)
        self.create_task_input(main_frame)
        self.create_task_list(main_frame)
        self.create_status_bar(main_frame)
        
        # Center window after creation
        self.center_window()
    
    def center_window(self):
        # Update window to calculate size needed
        self.window.update_idletasks()
        width = 850
        height = 700
        
        # Calculate center position
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        
        # Set window size and position
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="📝 TODO Application",
            font=("Segoe UI", 20, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(side="left")
        
        subtitle_label = tk.Label(
            header_frame,
            text="💾 SQLite Database Learning Project",
            font=("Segoe UI", 10),
            fg="#7f8c8d"
        )
        subtitle_label.pack(side="left", padx=(20, 0))
    
    def create_toolbar(self, parent):
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Filter buttons
        filter_label = ttk.Label(toolbar_frame, text="Filter:")
        filter_label.pack(side="left", padx=(0, 10))
        
        # Filter variable
        self.filter_var = tk.StringVar(value="all")
        
        filter_options = [
            ("All Tasks", "all"),
            ("Pending", "pending"),
            ("Completed", "completed")
        ]
        
        for text, value in filter_options:
            radio = ttk.Radiobutton(
                toolbar_frame,
                text=text,
                variable=self.filter_var,
                value=value,
                command=self.on_filter_change
            )
            radio.pack(side="left", padx=(0, 10))
        
        # Action buttons
        button_frame = ttk.Frame(toolbar_frame)
        button_frame.pack(side="right")
        
        refresh_btn = ttk.Button(
            button_frame,
            text="🔄 Refresh",
            command=self.refresh_task_list
        )
        refresh_btn.pack(side="left", padx=(0, 5))
        
        stats_btn = ttk.Button(
            button_frame,
            text="📊 Statistics",
            command=self.show_statistics
        )
        stats_btn.pack(side="left", padx=(0, 5))
        
        clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Clear Completed",
            command=self.clear_completed
        )
        clear_btn.pack(side="left")
    
    def create_task_input(self, parent):
        input_frame = ttk.LabelFrame(parent, text="Add New Task", padding="10")
        input_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        # Task input
        task_label = ttk.Label(input_frame, text="Task:")
        task_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.task_entry = ttk.Entry(input_frame, font=("Segoe UI", 11))
        self.task_entry.grid(row=0, column=1, sticky="ew", pady=(0, 5), padx=(10, 0))
        
        # Description input
        desc_label = ttk.Label(input_frame, text="Description:")
        desc_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        self.desc_entry = ttk.Entry(input_frame, font=("Segoe UI", 11))
        self.desc_entry.grid(row=1, column=1, sticky="ew", pady=(0, 5), padx=(10, 0))
        
        # Priority selection
        priority_label = ttk.Label(input_frame, text="Priority:")
        priority_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        priority_frame = ttk.Frame(input_frame)
        priority_frame.grid(row=2, column=1, sticky="w", pady=(0, 5), padx=(10, 0))
        
        self.priority_var = tk.StringVar(value="medium")
        
        priorities = [("🟢 Low", "low"), ("🟡 Medium", "medium"), ("🔴 High", "high")]
        for text, value in priorities:
            radio = ttk.Radiobutton(
                priority_frame,
                text=text,
                variable=self.priority_var,
                value=value
            )
            radio.pack(side="left", padx=(0, 15))
        
        # Add button
        add_btn = ttk.Button(
            input_frame,
            text="➕ Add Task",
            command=self.add_task,
            style="Accent.TButton"
        )
        add_btn.grid(row=3, column=1, sticky="e", pady=(10, 0), padx=(10, 0))
        
        # Bind Enter key to add task
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        self.desc_entry.bind('<Return>', lambda e: self.add_task())
        
        # Configure grid weights
        input_frame.columnconfigure(1, weight=1)
    
    def create_task_list(self, parent):
        list_frame = ttk.LabelFrame(parent, text="Tasks", padding="10")
        list_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        
        # Create Treeview with columns
        columns = ("ID", "Task", "Description", "Priority", "Status", "Created")
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        # Configure column headings and widths
        column_config = {
            "ID": (50, "center"),
            "Task": (200, "w"),
            "Description": (250, "w"),
            "Priority": (80, "center"),
            "Status": (100, "center"),
            "Created": (150, "center")
        }
        
        for col, (width, anchor) in column_config.items():
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=width, anchor=anchor)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.task_tree.xview)
        self.task_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.task_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Task action buttons
        action_frame = ttk.Frame(list_frame)
        action_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        
        edit_btn = ttk.Button(
            action_frame,
            text="📝 Edit",
            command=self.edit_task
        )
        edit_btn.pack(side="left", padx=(0, 5))
        
        toggle_btn = ttk.Button(
            action_frame,
            text="✅ Toggle Complete",
            command=self.toggle_completion
        )
        toggle_btn.pack(side="left", padx=(0, 5))
        
        delete_btn = ttk.Button(
            action_frame,
            text="🗑️ Delete",
            command=self.delete_task
        )
        delete_btn.pack(side="left", padx=(0, 5))
        
        search_frame = ttk.Frame(action_frame)
        search_frame.pack(side="right")
        
        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side="left", padx=(0, 5))
        
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side="left", padx=(0, 5))
        
        search_btn = ttk.Button(
            search_frame,
            text="🔍",
            command=self.search_tasks,
            width=3
        )
        search_btn.pack(side="left")
        
        # Bind search on Enter
        self.search_entry.bind('<Return>', lambda e: self.search_tasks())
        
        # Configure grid weights
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Bind double-click to edit
        self.task_tree.bind('<Double-1>', lambda e: self.edit_task())
    
    def create_status_bar(self, parent):
        self.status_frame = ttk.Frame(parent)
        self.status_frame.grid(row=4, column=0, sticky="ew")
        
        db_name = os.path.basename(self.db.db_path)
        self.status_label = ttk.Label(
            self.status_frame,
            text=f"Ready | Database: {db_name}",
            font=("Segoe UI", 9)
        )
        self.status_label.pack(side="left")
        
        self.task_count_label = ttk.Label(
            self.status_frame,
            text="",
            font=("Segoe UI", 9)
        )
        self.task_count_label.pack(side="right")
        
        # Configure main grid weights
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(3, weight=1)
    
    def add_task(self):
        # Get input values
        task = self.task_entry.get().strip()
        description = self.desc_entry.get().strip()
        priority = self.priority_var.get()
        
        if not task:
            messagebox.showwarning("Input Error", "Task title cannot be empty!")
            self.task_entry.focus()
            return
        
        # Add to database
        if self.db.add_task(task, description, priority):
            # Clear input fields
            self.task_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.priority_var.set("medium")
            
            # Refresh list
            self.refresh_task_list()
            self.update_status("Task added successfully!")
            
            # Focus back to task entry
            self.task_entry.focus()
        else:
            messagebox.showerror("Database Error", "Failed to add task!")
    
    def refresh_task_list(self):
        # Clear current items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Get tasks based on current filter
        if self.current_filter == "all":
            tasks = self.db.get_all_tasks()
        elif self.current_filter == "completed":
            tasks = self.db.get_tasks_by_status(True)
        elif self.current_filter == "pending":
            tasks = self.db.get_tasks_by_status(False)
        
        # Populate tree
        for task in tasks:
            task_id, title, desc, completed, priority, created, completed_date = task
            
            # Format status
            status = "✅ Completed" if completed else "⏳ Pending"
            
            # Format priority with icons
            priority_icons = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}
            priority_display = priority_icons.get(priority, priority)
            
            # Format date
            created_display = created.split()[0] if created else ""
            
            # Insert item
            item = self.task_tree.insert("", "end", values=(
                task_id, title, desc or "", priority_display, status, created_display
            ))
            
            # Color coding for completed tasks
            if completed:
                self.task_tree.set(item, "Task", f"✅ {title}")
        
        # Update task count
        total = len(tasks)
        completed = len([t for t in tasks if t[3]])
        pending = total - completed
        
        count_text = f"Total: {total} | Completed: {completed} | Pending: {pending}"
        self.task_count_label.config(text=count_text)
    
    def on_filter_change(self):
        # Update current filter and refresh list
        self.current_filter = self.filter_var.get()
        self.refresh_task_list()
        self.update_status(f"Filter changed to: {self.current_filter}")
    
    def get_selected_task_id(self):
        # Get selected task ID
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a task!")
            return None
        
        item = selection[0]
        task_id = self.task_tree.item(item)["values"][0]
        return int(task_id)
    
    def edit_task(self):
        task_id = self.get_selected_task_id()
        if not task_id:
            return
        
        # Get current task data
        tasks = self.db.get_all_tasks()
        current_task = None
        for task in tasks:
            if task[0] == task_id:
                current_task = task
                break
        
        if not current_task:
            messagebox.showerror("Error", "Task not found!")
            return
        
        # Create edit dialog
        dialog = EditTaskDialog(self.window, current_task)
        
        if dialog.result:
            # Update task in database
            updates = dialog.result
            if self.db.update_task(task_id, **updates):
                self.refresh_task_list()
                self.update_status("Task updated successfully!")
            else:
                messagebox.showerror("Database Error", "Failed to update task!")
    
    def toggle_completion(self):
        task_id = self.get_selected_task_id()
        if not task_id:
            return
        
        # Get current status
        tasks = self.db.get_all_tasks()
        current_task = None
        for task in tasks:
            if task[0] == task_id:
                current_task = task
                break
        
        if not current_task:
            messagebox.showerror("Error", "Task not found!")
            return
        
        # Toggle status
        new_status = not current_task[3]
        
        if self.db.mark_completed(task_id, new_status):
            self.refresh_task_list()
            action = "completed" if new_status else "pending"
            self.update_status(f"Task marked as {action}!")
        else:
            messagebox.showerror("Database Error", "Failed to update task status!")
    
    def delete_task(self):
        task_id = self.get_selected_task_id()
        if not task_id:
            return
        
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete task #{task_id}?"
        )
        
        if result:
            if self.db.delete_task(task_id):
                self.refresh_task_list()
                self.update_status("Task deleted successfully!")
            else:
                messagebox.showerror("Database Error", "Failed to delete task!")
    
    def search_tasks(self):
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            # If empty, refresh normal list
            self.refresh_task_list()
            return
        
        # Clear current items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Search and display results
        tasks = self.db.search_tasks(search_term)
        
        for task in tasks:
            task_id, title, desc, completed, priority, created, completed_date = task
            
            status = "✅ Completed" if completed else "⏳ Pending"
            priority_icons = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}
            priority_display = priority_icons.get(priority, priority)
            created_display = created.split()[0] if created else ""
            
            self.task_tree.insert("", "end", values=(
                task_id, title, desc or "", priority_display, status, created_display
            ))
        
        self.update_status(f"Found {len(tasks)} tasks matching '{search_term}'")
    
    def show_statistics(self):
        stats = self.db.get_task_stats()
        
        if not stats:
            messagebox.showerror("Error", "Unable to retrieve statistics!")
            return
        
        # Create statistics dialog
        StatsDialog(self.window, stats)
    
    def clear_completed(self):
        # Get completed task count
        completed_tasks = self.db.get_tasks_by_status(True)
        count = len(completed_tasks)
        
        if count == 0:
            messagebox.showinfo("Info", "No completed tasks to clear!")
            return
        
        result = messagebox.askyesno(
            "Confirm Clear",
            f"Are you sure you want to delete all {count} completed tasks?"
        )
        
        if result:
            deleted = self.db.clear_completed_tasks()
            self.refresh_task_list()
            self.update_status(f"Deleted {deleted} completed tasks!")
    
    def update_status(self, message):
        # Update status bar message
        self.status_label.config(text=message)
        # Reset to default after 3 seconds
        db_name = os.path.basename(self.db.db_path)
        self.window.after(3000, lambda: self.status_label.config(text=f"Ready | Database: {db_name}"))
    
    def run(self):
        # Start the application
        self.window.mainloop()


class EditTaskDialog:
    def __init__(self, parent, task_data):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Task")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Make modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 150
        self.dialog.geometry(f"400x300+{x}+{y}")
        
        self.create_widgets(task_data)
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_widgets(self, task_data):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        task_id, title, desc, completed, priority, created, completed_date = task_data
        
        # Task title
        ttk.Label(main_frame, text="Task Title:").pack(anchor="w", pady=(0, 5))
        self.task_entry = ttk.Entry(main_frame, font=("Segoe UI", 11))
        self.task_entry.pack(fill="x", pady=(0, 15))
        self.task_entry.insert(0, title)
        
        # Description
        ttk.Label(main_frame, text="Description:").pack(anchor="w", pady=(0, 5))
        self.desc_entry = ttk.Entry(main_frame, font=("Segoe UI", 11))
        self.desc_entry.pack(fill="x", pady=(0, 15))
        self.desc_entry.insert(0, desc or "")
        
        # Priority
        ttk.Label(main_frame, text="Priority:").pack(anchor="w", pady=(0, 5))
        
        self.priority_var = tk.StringVar(value=priority)
        priority_frame = ttk.Frame(main_frame)
        priority_frame.pack(fill="x", pady=(0, 20))
        
        priorities = [("🟢 Low", "low"), ("🟡 Medium", "medium"), ("🔴 High", "high")]
        for text, value in priorities:
            radio = ttk.Radiobutton(
                priority_frame,
                text=text,
                variable=self.priority_var,
                value=value
            )
            radio.pack(side="left", padx=(0, 15))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        save_btn = ttk.Button(
            button_frame,
            text="💾 Save",
            command=self.save_changes
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ttk.Button(
            button_frame,
            text="❌ Cancel",
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="left")
        
        # Focus on task entry
        self.task_entry.focus()
        self.task_entry.select_range(0, tk.END)
    
    def save_changes(self):
        task = self.task_entry.get().strip()
        
        if not task:
            messagebox.showwarning("Input Error", "Task title cannot be empty!")
            return
        
        self.result = {
            'task': task,
            'description': self.desc_entry.get().strip(),
            'priority': self.priority_var.get()
        }
        
        self.dialog.destroy()


class StatsDialog:
    def __init__(self, parent, stats):
        # Create dialog window
        dialog = tk.Toplevel(parent)
        dialog.title("📊 Task Statistics")
        dialog.geometry("350x250")
        dialog.resizable(False, False)
        
        # Make modal
        dialog.transient(parent)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 175
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 125
        dialog.geometry(f"350x250+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="📊 Task Statistics",
            font=("Segoe UI", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # Statistics
        stats_text = f"""📋 Total tasks: {stats['total']}
✅ Completed: {stats['completed']}
⏳ Pending: {stats['pending']}
📈 Completion rate: {stats['completion_rate']:.1f}%"""
        
        stats_label = tk.Label(
            main_frame,
            text=stats_text,
            font=("Segoe UI", 11),
            justify="left"
        )
        stats_label.pack(pady=(0, 15))
        
        # Priority breakdown
        if stats['priority_counts']:
            priority_text = "🎯 Pending tasks by priority:\n"
            priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            
            for priority, count in stats['priority_counts'].items():
                icon = priority_icons.get(priority, "⚪")
                priority_text += f"    {icon} {priority.capitalize()}: {count}\n"
            
            priority_label = tk.Label(
                main_frame,
                text=priority_text,
                font=("Segoe UI", 10),
                justify="left"
            )
            priority_label.pack()
        
        # Close button
        close_btn = ttk.Button(
            main_frame,
            text="✅ Close",
            command=dialog.destroy
        )
        close_btn.pack(pady=(20, 0))


def main():
    """Main function"""
    try:
        app = TodoGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")


if __name__ == "__main__":
    main()