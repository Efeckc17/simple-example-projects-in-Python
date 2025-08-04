import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import json
import threading
from datetime import datetime

# Add parent directory to path to import core module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from speedtest_core import SpeedTestCore


class SpeedTestGUI:
    
    def __init__(self):
        # Create main window
        self.window = tk.Tk()
        self.setup_window()
        
        # Initialize speedtest core
        self.speed_test = SpeedTestCore()
        
        # Set up history file path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.history_file = os.path.join(script_dir, "speedtest_history.json")
        
        # Load test history
        self.test_history = self.load_history()
        
        # Test state
        self.is_testing = False
        self.current_results = {}
        
        # Create GUI components
        self.create_widgets()
        
        # Initialize display
        self.update_history_display()
    
    def setup_window(self):
        self.window.title("🌐 Internet Speed Test")
        self.window.resizable(True, True)
        self.window.minsize(700, 600)
        
        # Apply modern theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for progress bars
        style.configure("Download.Horizontal.TProgressbar", background='#28a745')
        style.configure("Upload.Horizontal.TProgressbar", background='#fd7e14')
        style.configure("Overall.Horizontal.TProgressbar", background='#007bff')
    
    def create_widgets(self):
        # Configure main window grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # Main container
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.create_header(main_frame)
        self.create_test_section(main_frame)
        self.create_results_section(main_frame)
        self.create_history_section(main_frame)
        self.create_status_bar(main_frame)
        
        # Center window after creation
        self.center_window()
    
    def center_window(self):
        # Update window to calculate size needed
        self.window.update_idletasks()
        width = 750
        height = 650
        
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
            text="🌐 Internet Speed Test",
            font=("Segoe UI", 22, "bold"),
            fg="#2c3e50"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="💾 Powered by Speedtest.net",
            font=("Segoe UI", 10),
            fg="#7f8c8d"
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_test_section(self, parent):
        test_frame = ttk.LabelFrame(parent, text="Speed Test", padding="15")
        test_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Start test button
        self.test_button = ttk.Button(
            test_frame,
            text="🚀 Start Speed Test",
            command=self.start_speed_test,
            style="Accent.TButton"
        )
        self.test_button.pack(pady=(0, 15))
        
        # Progress bars
        progress_frame = ttk.Frame(test_frame)
        progress_frame.pack(fill="x", pady=(0, 15))
        
        # Overall progress
        ttk.Label(progress_frame, text="Overall Progress:").pack(anchor="w")
        self.overall_progress = ttk.Progressbar(
            progress_frame,
            style="Overall.Horizontal.TProgressbar",
            length=400,
            mode='determinate'
        )
        self.overall_progress.pack(fill="x", pady=(2, 10))
        
        # Status label
        self.status_label = tk.Label(
            progress_frame,
            text="Ready to test",
            font=("Segoe UI", 10),
            fg="#6c757d"
        )
        self.status_label.pack()
        
        test_frame.columnconfigure(0, weight=1)
    
    def create_results_section(self, parent):
        results_frame = ttk.LabelFrame(parent, text="Latest Results", padding="15")
        results_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        # Results grid
        results_grid = ttk.Frame(results_frame)
        results_grid.pack(fill="x")
        
        # Download speed
        download_frame = ttk.Frame(results_grid)
        download_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.download_icon = tk.Label(
            download_frame,
            text="📥",
            font=("Segoe UI", 24)
        )
        self.download_icon.pack()
        
        ttk.Label(download_frame, text="Download", font=("Segoe UI", 10)).pack()
        
        self.download_value = tk.Label(
            download_frame,
            text="-- Mbps",
            font=("Segoe UI", 16, "bold"),
            fg="#28a745"
        )
        self.download_value.pack()
        
        # Upload speed
        upload_frame = ttk.Frame(results_grid)
        upload_frame.grid(row=0, column=1, sticky="ew", padx=(10, 10))
        
        self.upload_icon = tk.Label(
            upload_frame,
            text="📤",
            font=("Segoe UI", 24)
        )
        self.upload_icon.pack()
        
        ttk.Label(upload_frame, text="Upload", font=("Segoe UI", 10)).pack()
        
        self.upload_value = tk.Label(
            upload_frame,
            text="-- Mbps",
            font=("Segoe UI", 16, "bold"),
            fg="#fd7e14"
        )
        self.upload_value.pack()
        
        # Ping
        ping_frame = ttk.Frame(results_grid)
        ping_frame.grid(row=0, column=2, sticky="ew", padx=(10, 0))
        
        self.ping_icon = tk.Label(
            ping_frame,
            text="🏓",
            font=("Segoe UI", 24)
        )
        self.ping_icon.pack()
        
        ttk.Label(ping_frame, text="Ping", font=("Segoe UI", 10)).pack()
        
        self.ping_value = tk.Label(
            ping_frame,
            text="-- ms",
            font=("Segoe UI", 16, "bold"),
            fg="#007bff"
        )
        self.ping_value.pack()
        
        # Configure grid weights
        results_grid.columnconfigure(0, weight=1)
        results_grid.columnconfigure(1, weight=1)
        results_grid.columnconfigure(2, weight=1)
        
        # Additional info
        info_frame = ttk.Frame(results_frame)
        info_frame.pack(fill="x", pady=(15, 0))
        
        self.server_label = tk.Label(
            info_frame,
            text="Server: Not tested",
            font=("Segoe UI", 9),
            fg="#6c757d"
        )
        self.server_label.pack(side="left")
        
        self.rating_label = tk.Label(
            info_frame,
            text="",
            font=("Segoe UI", 9, "bold"),
            fg="#28a745"
        )
        self.rating_label.pack(side="right")
        
        results_frame.columnconfigure(0, weight=1)
    
    def create_history_section(self, parent):
        history_frame = ttk.LabelFrame(parent, text="Test History", padding="10")
        history_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        
        # History controls
        controls_frame = ttk.Frame(history_frame)
        controls_frame.pack(fill="x", pady=(0, 10))
        
        refresh_btn = ttk.Button(
            controls_frame,
            text="🔄 Refresh",
            command=self.update_history_display
        )
        refresh_btn.pack(side="left")
        
        clear_btn = ttk.Button(
            controls_frame,
            text="🗑️ Clear History",
            command=self.clear_history
        )
        clear_btn.pack(side="left", padx=(10, 0))
        
        stats_btn = ttk.Button(
            controls_frame,
            text="📊 Statistics",
            command=self.show_statistics
        )
        stats_btn.pack(side="right")
        
        # History tree
        columns = ("Time", "Download", "Upload", "Ping", "Server")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        column_config = {
            "Time": (120, "center"),
            "Download": (100, "center"),
            "Upload": (100, "center"),
            "Ping": (80, "center"),
            "Server": (200, "w")
        }
        
        for col, (width, anchor) in column_config.items():
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=width, anchor=anchor)
        
        # Scrollbar for history
        history_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        history_scrollbar.pack(side="right", fill="y")
        
        # Configure grid weights
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(1, weight=1)
        
        parent.rowconfigure(3, weight=1)
    
    def create_status_bar(self, parent):
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=4, column=0, sticky="ew")
        
        self.status_bar_label = ttk.Label(
            status_frame,
            text=f"Ready | Tests in history: {len(self.test_history)}",
            font=("Segoe UI", 9)
        )
        self.status_bar_label.pack(side="left")
        
        timestamp_label = ttk.Label(
            status_frame,
            text=datetime.now().strftime("%Y-%m-%d %H:%M"),
            font=("Segoe UI", 9)
        )
        timestamp_label.pack(side="right")
        
        parent.columnconfigure(0, weight=1)
    
    def start_speed_test(self):
        """Start speed test in background thread"""
        if self.is_testing:
            return
        
        # Confirm test start
        result = messagebox.askyesno(
            "Start Speed Test",
            "This test may take 30-60 seconds and will use your internet bandwidth.\n\nStart the test?"
        )
        
        if not result:
            return
        
        # Reset UI
        self.reset_results_display()
        self.is_testing = True
        
        # Update button
        self.test_button.config(text="⏳ Testing...", state="disabled")
        
        # Set up callbacks
        self.speed_test.set_callbacks(self.progress_callback, self.status_callback)
        
        # Start test in background thread
        self.speed_test.run_test_threaded(self.test_completed_callback)
    
    def progress_callback(self, progress: float, message: str):
        """Callback for progress updates - runs in background thread"""
        # Schedule UI update in main thread
        self.window.after(0, lambda: self.update_progress_ui(progress, message))
    
    def status_callback(self, status: str):
        """Callback for status updates - runs in background thread"""
        # Schedule UI update in main thread
        self.window.after(0, lambda: self.update_status_ui(status))
    
    def test_completed_callback(self, results: dict):
        """Callback when test is completed - runs in background thread"""
        # Schedule UI update in main thread
        self.window.after(0, lambda: self.handle_test_completion(results))
    
    def update_progress_ui(self, progress: float, message: str):
        """Update progress bar and message in UI thread"""
        self.overall_progress['value'] = progress
        if message:
            self.status_label.config(text=message)
    
    def update_status_ui(self, status: str):
        """Update status label in UI thread"""
        self.status_label.config(text=status)
    
    def handle_test_completion(self, results: dict):
        """Handle test completion in UI thread"""
        self.is_testing = False
        
        # Reset button
        self.test_button.config(text="🚀 Start Speed Test", state="normal")
        
        if results:
            # Store results
            self.current_results = results
            
            # Update results display
            self.update_results_display(results)
            
            # Save to history
            self.save_test_result(results)
            
            # Update history display
            self.update_history_display()
            
            # Update status bar
            self.update_status_bar()
            
            # Show completion message
            self.status_label.config(text="✅ Test completed successfully!")
            
        else:
            messagebox.showerror("Test Failed", "Speed test failed! Please check your internet connection.")
            self.status_label.config(text="❌ Test failed")
    
    def reset_results_display(self):
        """Reset results display for new test"""
        self.download_value.config(text="-- Mbps")
        self.upload_value.config(text="-- Mbps")
        self.ping_value.config(text="-- ms")
        self.server_label.config(text="Server: Testing...")
        self.rating_label.config(text="")
        self.overall_progress['value'] = 0
    
    def update_results_display(self, results: dict):
        """Update results display with test results"""
        download = results.get('download_mbps', 0)
        upload = results.get('upload_mbps', 0)
        ping = results.get('ping_ms', 0)
        
        # Update values
        self.download_value.config(text=self.speed_test.format_speed(download))
        self.upload_value.config(text=self.speed_test.format_speed(upload))
        self.ping_value.config(text=f"{ping:.1f} ms")
        
        # Update server info
        server_location = results.get('server_location', 'Unknown')
        self.server_label.config(text=f"Server: {server_location}")
        
        # Update rating
        rating = self.speed_test.get_speed_rating(download)
        self.rating_label.config(text=rating)
        
        # Set progress to 100%
        self.overall_progress['value'] = 100
    
    def update_history_display(self):
        """Update history tree view"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add recent tests (last 20)
        recent_tests = self.test_history[-20:] if len(self.test_history) > 20 else self.test_history
        
        for test in reversed(recent_tests):
            timestamp = test.get('timestamp', 'Unknown')
            download = self.speed_test.format_speed(test.get('download_mbps', 0))
            upload = self.speed_test.format_speed(test.get('upload_mbps', 0))
            ping = f"{test.get('ping_ms', 0):.1f} ms"
            server = test.get('server_location', 'Unknown')
            
            # Format timestamp
            try:
                dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                time_str = dt.strftime('%m/%d %H:%M')
            except:
                time_str = timestamp
            
            self.history_tree.insert("", "end", values=(time_str, download, upload, ping, server))
    
    def update_status_bar(self):
        """Update status bar with current info"""
        test_count = len(self.test_history)
        self.status_bar_label.config(text=f"Ready | Tests in history: {test_count}")
    
    def clear_history(self):
        """Clear test history"""
        if not self.test_history:
            messagebox.showinfo("No History", "No test history to clear!")
            return
        
        result = messagebox.askyesno(
            "Clear History",
            f"Are you sure you want to clear all {len(self.test_history)} test results?"
        )
        
        if result:
            self.test_history = []
            self.save_history()
            self.update_history_display()
            self.update_status_bar()
            messagebox.showinfo("History Cleared", "Test history has been cleared!")
    
    def show_statistics(self):
        """Show statistics dialog"""
        if not self.test_history:
            messagebox.showinfo("No Data", "No test history available for statistics!")
            return
        
        StatsDialog(self.window, self.test_history, self.speed_test)
    
    def load_history(self) -> list:
        """Load test history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading history: {e}")
            return []
    
    def save_history(self):
        """Save test history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.test_history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def save_test_result(self, results: dict):
        """Save test result to history"""
        self.test_history.append(results)
        # Keep only last 100 tests
        self.test_history = self.test_history[-100:]
        self.save_history()
    
    def run(self):
        """Start the application"""
        self.window.mainloop()


class StatsDialog:
    def __init__(self, parent, test_history, speed_test_core):
        # Create dialog window
        dialog = tk.Toplevel(parent)
        dialog.title("📊 Speed Test Statistics")
        dialog.geometry("450x350")
        dialog.resizable(False, False)
        
        # Make modal
        dialog.transient(parent)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 225
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 175
        dialog.geometry(f"450x350+{x}+{y}")
        
        self.create_widgets(dialog, test_history, speed_test_core)
    
    def create_widgets(self, dialog, test_history, speed_test_core):
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="📊 Speed Test Statistics",
            font=("Segoe UI", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # Calculate statistics
        downloads = [t.get('download_mbps', 0) for t in test_history]
        uploads = [t.get('upload_mbps', 0) for t in test_history]
        pings = [t.get('ping_ms', 0) for t in test_history if t.get('ping_ms', 0) > 0]
        
        stats_text = f"📋 Total Tests: {len(test_history)}\n\n"
        
        if downloads:
            avg_download = sum(downloads) / len(downloads)
            max_download = max(downloads)
            min_download = min(downloads)
            
            stats_text += f"📥 Download Statistics:\n"
            stats_text += f"   Average: {speed_test_core.format_speed(avg_download)}\n"
            stats_text += f"   Maximum: {speed_test_core.format_speed(max_download)}\n"
            stats_text += f"   Minimum: {speed_test_core.format_speed(min_download)}\n\n"
        
        if uploads:
            avg_upload = sum(uploads) / len(uploads)
            max_upload = max(uploads)
            min_upload = min(uploads)
            
            stats_text += f"📤 Upload Statistics:\n"
            stats_text += f"   Average: {speed_test_core.format_speed(avg_upload)}\n"
            stats_text += f"   Maximum: {speed_test_core.format_speed(max_upload)}\n"
            stats_text += f"   Minimum: {speed_test_core.format_speed(min_upload)}\n\n"
        
        if pings:
            avg_ping = sum(pings) / len(pings)
            max_ping = max(pings)
            min_ping = min(pings)
            
            stats_text += f"🏓 Ping Statistics:\n"
            stats_text += f"   Average: {avg_ping:.1f} ms\n"
            stats_text += f"   Maximum: {max_ping:.1f} ms\n"
            stats_text += f"   Minimum: {min_ping:.1f} ms\n\n"
        
        # Latest test performance
        if test_history:
            latest = test_history[-1]
            latest_download = latest.get('download_mbps', 0)
            rating = speed_test_core.get_speed_rating(latest_download)
            stats_text += f"⭐ Latest Test Rating: {rating}"
        
        # Statistics display
        stats_label = tk.Label(
            main_frame,
            text=stats_text,
            font=("Segoe UI", 11),
            justify="left",
            anchor="nw"
        )
        stats_label.pack(fill="both", expand=True)
        
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
        app = SpeedTestGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")


if __name__ == "__main__":
    main()