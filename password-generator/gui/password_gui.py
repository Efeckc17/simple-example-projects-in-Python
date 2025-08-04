import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip


class PasswordGeneratorGUI:
    
    def __init__(self):
        # Create main window
        self.window = tk.Tk()
        self.setup_window()
        
        # Define character sets for password generation
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Initialize GUI components
        self.create_widgets()
    
    def setup_window(self):
        self.window.title("🔐 Password Generator")
        # Allow window resizing for better user experience
        self.window.resizable(True, True)
        # Set minimum size to prevent UI breaking
        self.window.minsize(400, 500)
        
        # Apply modern theme
        style = ttk.Style()
        style.theme_use('clam')
    
    def create_widgets(self):
        # Configure window grid to expand with content
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # Main container with padding
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Create UI sections in order
        self.create_header(main_frame)
        self.create_options(main_frame)
        self.create_controls(main_frame)
        self.create_display(main_frame)
        
        # Center window after all widgets are created
        self.center_window()
    
    def center_window(self):
        # Update window to calculate actual size needed
        self.window.update_idletasks()
        width = self.window.winfo_reqwidth()
        height = self.window.winfo_reqheight()
        
        # Calculate center position
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        
        # Set window size and position
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="ew")
        
        title_label = tk.Label(
            header_frame,
            text="🔐 Password Generator",
            font=("Segoe UI", 24, "bold"),
            fg="#2c3e50"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Generate secure passwords with custom options",
            font=("Segoe UI", 12),
            fg="#7f8c8d"
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_options(self, parent):
        options_frame = ttk.LabelFrame(parent, text="Password Options", padding="15")
        options_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        ttk.Label(options_frame, text="Password Length:").grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        length_frame = ttk.Frame(options_frame)
        length_frame.grid(row=0, column=1, sticky="ew", pady=(0, 10))
        
        # Variable to store password length
        self.length_var = tk.IntVar(value=12)
        # Scale widget for length selection
        self.length_scale = ttk.Scale(
            length_frame,
            from_=8,
            to=128,
            variable=self.length_var,
            orient="horizontal",
            command=self.update_length_label
        )
        self.length_scale.pack(side="left", fill="x", expand=True)
        
        self.length_label = ttk.Label(length_frame, text="12")
        self.length_label.pack(side="right", padx=(10, 0))
        
        ttk.Label(options_frame, text="Character Types:").grid(row=1, column=0, sticky="nw", pady=(10, 0))
        
        checkboxes_frame = ttk.Frame(options_frame)
        checkboxes_frame.grid(row=1, column=1, sticky="ew", pady=(10, 0))
        
        # Boolean variables for checkboxes
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(checkboxes_frame, text="Uppercase Letters (A-Z)", 
                       variable=self.use_uppercase).pack(anchor="w")
        ttk.Checkbutton(checkboxes_frame, text="Numbers (0-9)", 
                       variable=self.use_digits).pack(anchor="w")
        ttk.Checkbutton(checkboxes_frame, text="Symbols (!@#$%...)", 
                       variable=self.use_symbols).pack(anchor="w")
        ttk.Checkbutton(checkboxes_frame, text="Exclude Ambiguous (0,O,1,l)", 
                       variable=self.exclude_ambiguous).pack(anchor="w")
        
        options_frame.columnconfigure(1, weight=1)
    
    def create_controls(self, parent):
        controls_frame = ttk.Frame(parent)
        controls_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        ttk.Label(controls_frame, text="Generate:").pack(side="left")
        
        self.count_var = tk.IntVar(value=1)
        count_spinbox = ttk.Spinbox(
            controls_frame,
            from_=1,
            to=10,
            width=5,
            textvariable=self.count_var
        )
        count_spinbox.pack(side="left", padx=(10, 5))
        
        ttk.Label(controls_frame, text="passwords").pack(side="left")
        
        generate_btn = ttk.Button(
            controls_frame,
            text="🔐 Generate",
            command=self.generate_passwords,
            style="Accent.TButton"
        )
        generate_btn.pack(side="right", padx=(20, 0))
        
        clear_btn = ttk.Button(
            controls_frame,
            text="🗑️ Clear",
            command=self.clear_display
        )
        clear_btn.pack(side="right")
    
    def create_display(self, parent):
        display_frame = ttk.LabelFrame(parent, text="Generated Passwords", padding="15")
        display_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")
        
        # Text widget for displaying generated passwords
        self.passwords_text = tk.Text(
            display_frame,
            height=12,
            width=60,
            font=("Consolas", 11),
            wrap="word",
            state="disabled"  # Read-only by default
        )
        
        # Scrollbar for long password lists
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.passwords_text.yview)
        self.passwords_text.configure(yscrollcommand=scrollbar.set)
        
        self.passwords_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        buttons_frame = ttk.Frame(display_frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        
        copy_btn = ttk.Button(
            buttons_frame,
            text="📋 Copy All",
            command=self.copy_all_passwords
        )
        copy_btn.pack(side="left")
        
        copy_last_btn = ttk.Button(
            buttons_frame,
            text="📋 Copy Last",
            command=self.copy_last_password
        )
        copy_last_btn.pack(side="left", padx=(10, 0))
        
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(3, weight=1)
    
    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))
    
    def generate_password(self, length, use_uppercase, use_digits, use_symbols, exclude_ambiguous):
        charset = self.lowercase
        
        if use_uppercase:
            charset += self.uppercase
        if use_digits:
            charset += self.digits
        if use_symbols:
            charset += self.symbols
        
        if exclude_ambiguous:
            ambiguous = "0O1l|"
            charset = ''.join(c for c in charset if c not in ambiguous)
        
        if not charset:
            raise ValueError("No character types selected")
        
        password = ''.join(random.choice(charset) for _ in range(length))
        return password
    
    def check_strength(self, password):
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Use at least 8 characters")
        
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
            
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
            
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Add numbers")
            
        if any(c in self.symbols for c in password):
            score += 1
        else:
            feedback.append("Add symbols")
        
        strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
        strength = strength_levels[min(score, 4)]
        
        return strength, feedback
    
    def generate_passwords(self):
        try:
            # Get user input values
            length = self.length_var.get()
            count = self.count_var.get()
            
            # Validate that at least one character type is selected
            if not any([True, self.use_uppercase.get(), self.use_digits.get(), self.use_symbols.get()]):
                messagebox.showerror("Error", "Please select at least one character type!")
                return
            
            # Enable text widget for editing
            self.passwords_text.config(state="normal")
            # Clear previous content
            self.passwords_text.delete(1.0, tk.END)
            
            # Store passwords for clipboard functionality
            self.generated_passwords = []
            
            for i in range(count):
                password = self.generate_password(
                    length,
                    self.use_uppercase.get(),
                    self.use_digits.get(),
                    self.use_symbols.get(),
                    self.exclude_ambiguous.get()
                )
                
                strength, feedback = self.check_strength(password)
                
                self.generated_passwords.append(password)
                
                self.passwords_text.insert(tk.END, f"Password {i+1}:\n")
                self.passwords_text.insert(tk.END, f"{password}\n")
                self.passwords_text.insert(tk.END, f"Strength: {strength}\n")
                
                if feedback:
                    self.passwords_text.insert(tk.END, f"Suggestions: {', '.join(feedback)}\n")
                
                self.passwords_text.insert(tk.END, "\n" + "-"*50 + "\n\n")
            
            # Make text widget read-only again
            self.passwords_text.config(state="disabled")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def clear_display(self):
        self.passwords_text.config(state="normal")
        self.passwords_text.delete(1.0, tk.END)
        self.passwords_text.config(state="disabled")
        self.generated_passwords = []
    
    def copy_all_passwords(self):
        # Check if passwords exist
        if hasattr(self, 'generated_passwords') and self.generated_passwords:
            # Join all passwords with newlines
            all_passwords = '\n'.join(self.generated_passwords)
            # Copy to system clipboard
            pyperclip.copy(all_passwords)
            messagebox.showinfo("Copied", f"{len(self.generated_passwords)} passwords copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No passwords to copy!")
    
    def copy_last_password(self):
        if hasattr(self, 'generated_passwords') and self.generated_passwords:
            last_password = self.generated_passwords[-1]
            pyperclip.copy(last_password)
            messagebox.showinfo("Copied", "Last password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No passwords to copy!")
    
    def run(self):
        self.window.mainloop()


def main():
    try:
        # Create and run the application
        app = PasswordGeneratorGUI()
        app.run()
    except ImportError:
        # Handle missing dependencies gracefully
        print("Error: pyperclip module is required for clipboard functionality")
        print("Install it with: pip install pyperclip")
    except Exception as e:
        print(f"Error starting application: {e}")


if __name__ == "__main__":
    main()