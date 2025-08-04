

import tkinter as tk
from tkinter import ttk, messagebox
import operator
from typing import Union, Optional
import math


class CalculatorGUI:
    
    def __init__(self):
        self.window = tk.Tk()
        self.setup_window()
        
        # Calculator state
        self.current_input = ""
        self.previous_input = ""
        self.operator = None
        self.result = 0
        self.should_reset = False
        
        # Operator List
        self.operations = {
            '+': operator.add,
            '-': operator.sub,
            '×': operator.mul,
            '÷': operator.truediv,
            '**': operator.pow,
            '%': operator.mod
        }
        
        self.create_widgets()
    
    def setup_window(self):
        """Sets up window properties"""
        self.window.title("🧮 GUI Calculator")
        self.window.geometry("350x500")
        self.window.resizable(False, False)
        
        # Center window
        self.window.eval('tk::PlaceWindow . center')
        
        # Theme settings
        style = ttk.Style()
        style.theme_use('clam')
        
        # Window icon (optional)
        try:
            self.window.iconbitmap("calculator.ico")
        except:
            pass  # No problem if icon doesn't exist
    
    def create_widgets(self):
        """Creates all widgets"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Display
        self.create_display(main_frame)
        
        # Button grid (Keypad)
        self.create_buttons(main_frame)
        
        # Keyboard shortcuts
        self.setup_keyboard_bindings()
    
    def create_display(self, parent):
        # Display frame
        display_frame = ttk.Frame(parent)
        display_frame.grid(row=0, column=0, columnspan=4, pady=(0, 20), sticky="ew")
        
        # Previous operation indicator
        self.prev_label = tk.Label(
            display_frame,
            text="",
            font=("Segoe UI", 10),
            fg="gray",
            bg="white",
            anchor="e",
            height=1
        )
        self.prev_label.pack(fill="x", padx=5, pady=(5, 0))
        
        # Main display
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Segoe UI", 20, "bold"),
            justify="right",
            state="readonly",
            relief="solid",
            bd=1,
            readonlybackground="white",
            fg="black"
        )
        self.display.pack(fill="x", padx=5, pady=5, ipady=10)
    
    def create_buttons(self, parent):
        """Creates the keypad"""
        # Button frame
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=1, column=0, columnspan=4)
        
        # Button style
        style = ttk.Style()
        
        # Number buttons style
        style.configure(
            "Number.TButton",
            font=("Segoe UI", 14, "bold"),
            padding=(5, 10)
        )
        
        # Operator buttons style
        style.configure(
            "Operator.TButton",
            font=("Segoe UI", 14, "bold"),
            padding=(5, 10)
        )
        
        # Function buttons style
        style.configure(
            "Function.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=(5, 10)
        )
        
        # Button definitions (row, column, text, color, command)
        buttons = [
            # Row 0 - Function keys
            (0, 0, "C", "Function.TButton", self.clear_all),
            (0, 1, "CE", "Function.TButton", self.clear_entry),
            (0, 2, "⌫", "Function.TButton", self.backspace),
            (0, 3, "÷", "Operator.TButton", lambda: self.set_operator("÷")),
            
            (1, 0, "7", "Number.TButton", lambda: self.add_digit("7")),
            (1, 1, "8", "Number.TButton", lambda: self.add_digit("8")),
            (1, 2, "9", "Number.TButton", lambda: self.add_digit("9")),
            (1, 3, "×", "Operator.TButton", lambda: self.set_operator("×")),
            
            (2, 0, "4", "Number.TButton", lambda: self.add_digit("4")),
            (2, 1, "5", "Number.TButton", lambda: self.add_digit("5")),
            (2, 2, "6", "Number.TButton", lambda: self.add_digit("6")),
            (2, 3, "-", "Operator.TButton", lambda: self.set_operator("-")),
            
            (3, 0, "1", "Number.TButton", lambda: self.add_digit("1")),
            (3, 1, "2", "Number.TButton", lambda: self.add_digit("2")),
            (3, 2, "3", "Number.TButton", lambda: self.add_digit("3")),
            (3, 3, "+", "Operator.TButton", lambda: self.set_operator("+")),
            
            (4, 0, "±", "Function.TButton", self.toggle_sign),
            (4, 1, "0", "Number.TButton", lambda: self.add_digit("0")),
            (4, 2, ".", "Number.TButton", self.add_decimal),
            (4, 3, "=", "Operator.TButton", self.calculate),
        ]
        
        # Create buttons
        self.buttons = {}
        for row, col, text, style_name, command in buttons:
            btn = ttk.Button(
                button_frame,
                text=text,
                style=style_name,
                command=command,
                width=6
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.buttons[text] = btn
        
        
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
        
        self.create_advanced_buttons(button_frame)
    
    def create_advanced_buttons(self, parent):
        """Advanced function buttons"""
        advanced_frame = ttk.Frame(parent)
        advanced_frame.grid(row=5, column=0, columnspan=4, pady=(10, 0))
        
        advanced_buttons = [
            ("√", self.square_root),
            ("x²", self.square),
            ("1/x", self.reciprocal),
            ("%", lambda: self.set_operator("%")),
        ]
        
        for i, (text, command) in enumerate(advanced_buttons):
            btn = ttk.Button(
                advanced_frame,
                text=text,
                style="Function.TButton",
                command=command,
                width=6
            )
            btn.grid(row=0, column=i, padx=2, pady=2)
    
    def setup_keyboard_bindings(self):
        
        self.window.bind('<Key>', self.key_press)
        self.window.focus_set()
        
        self.window.bind('<Control-c>', lambda e: self.clear_all())
        self.window.bind('<Escape>', lambda e: self.clear_all())
        self.window.bind('<BackSpace>', lambda e: self.backspace())
    
    def key_press(self, event):
        key = event.char
        
        
        if key.isdigit():
            self.add_digit(key)
        
        elif key == '+':
            self.set_operator('+')
        elif key == '-':
            self.set_operator('-')
        elif key in ['*', 'x', 'X']:
            self.set_operator('×')
        elif key in ['/', ':']:
            self.set_operator('÷')
        elif key in ['=', '\r']:  # Enter key
            self.calculate()
        elif key == '.':
            self.add_decimal()
        elif key == '%':
            self.set_operator('%')
    
    def add_digit(self, digit):
        if self.should_reset:
            self.current_input = ""
            self.should_reset = False
        
        if self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit
        
        self.update_display()
    
    def add_decimal(self):
        if self.should_reset:
            self.current_input = "0"
            self.should_reset = False
        
        if "." not in self.current_input:
            if not self.current_input:
                self.current_input = "0"
            self.current_input += "."
            self.update_display()
    
    def set_operator(self, op):
        if self.current_input:
            if self.operator and not self.should_reset:
                self.calculate()
            
            self.previous_input = self.current_input
            self.operator = op
            self.should_reset = True
            
            self.prev_label.config(text=f"{self.previous_input} {op}")
    
    def calculate(self):
        if not self.operator or not self.previous_input or not self.current_input:
            return
        
        try:
            prev_val = float(self.previous_input)
            curr_val = float(self.current_input)
            
            if self.operator == "÷" and curr_val == 0:
                raise ZeroDivisionError("Division by zero error")
            
            if self.operator in self.operations:
                result = self.operations[self.operator](prev_val, curr_val)
            else:
                result = curr_val
            
            if result == int(result):
                self.current_input = str(int(result))
            else:
                self.current_input = f"{result:.10g}"
            
            self.prev_label.config(
                text=f"{self.previous_input} {self.operator} {curr_val} ="
            )
            
            self.operator = None
            self.previous_input = ""
            self.should_reset = True
            
        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero error!")
            self.clear_all()
        except ValueError:
            messagebox.showerror("Error", "Invalid value!")
            self.clear_all()
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
            self.clear_all()
        
        self.update_display()
    
    def clear_all(self):
        """Clears everything (C)"""
        self.current_input = ""
        self.previous_input = ""
        self.operator = None
        self.should_reset = False
        self.prev_label.config(text="")
        self.display_var.set("0")
    
    def clear_entry(self):
        """Clears only current entry (CE)"""
        self.current_input = ""
        self.update_display()
    
    def backspace(self):
        """Deletes last character"""
        if self.current_input and not self.should_reset:
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.current_input = "0"
            self.update_display()
    
    def toggle_sign(self):
        """Changes sign (±)"""
        if self.current_input and self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.update_display()
    
    def square_root(self):
        """Calculates square root"""
        if self.current_input:
            try:
                value = float(self.current_input)
                if value < 0:
                    raise ValueError("Cannot calculate square root of negative number")
                
                result = math.sqrt(value)
                self.current_input = f"{result:.10g}"
                self.prev_label.config(text=f"√({value}) =")
                self.should_reset = True
                self.update_display()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def square(self):
        """Calculates square"""
        if self.current_input:
            try:
                value = float(self.current_input)
                result = value ** 2
                self.prev_label.config(text=f"{value}² =")
                self.current_input = f"{result:.10g}"
                self.should_reset = True
                self.update_display()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def reciprocal(self):
        """Calculates reciprocal (1/x)"""
        if self.current_input:
            try:
                value = float(self.current_input)
                if value == 0:
                    raise ZeroDivisionError("Cannot calculate reciprocal of zero")
                
                result = 1 / value
                self.prev_label.config(text=f"1/({value}) =")
                self.current_input = f"{result:.10g}"
                self.should_reset = True
                self.update_display()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def update_display(self):
        """Updates display"""
        if not self.current_input:
            self.display_var.set("0")
        else:
            self.display_var.set(self.current_input)
    
    def run(self):
        """Runs the application"""
        self.window.mainloop()


def main():
    """Main function"""
    app = CalculatorGUI()
    app.run()


if __name__ == "__main__":
    main()