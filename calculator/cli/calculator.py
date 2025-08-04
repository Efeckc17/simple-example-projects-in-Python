#!/usr/bin/env python3
"""
CLI Calculator - Simple Command Line Calculator
==============================================

Features:
- Basic math operations (+, -, *, /, **)
- Continuous calculation (use previous result)
- Clean and user-friendly interface
- Error handling
"""

import sys
import operator
from typing import Union, Optional


class Calculator:
    """Simple calculator class"""
    
    def __init__(self):
        self.memory: Optional[float] = None
        self.operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '**': operator.pow,
            '%': operator.mod
        }
    
    def calculate(self, expression: str) -> Union[float, str]:
        """
        Calculates the given expression
        
        Args:
            expression: Mathematical expression to calculate
            
        Returns:
            Calculation result or error message
        """
        expression = expression.strip().replace(' ', '')
        
        if not expression:
            return "Please enter an expression"
        
        # Check special commands
        if expression.lower() in ['quit', 'exit', 'q']:
            return 'quit'
        
        if expression.lower() in ['clear', 'c']:
            self.memory = None
            return "Memory cleared"
        
        if expression.lower() in ['memory', 'm']:
            return f"Memory: {self.memory if self.memory is not None else 'Empty'}"
        
        # Replace 'ans' with previous result if exists
        if 'ans' in expression.lower() and self.memory is not None:
            expression = expression.lower().replace('ans', str(self.memory))
        
        try:
            # Use safer method instead of raw eval for security
            result = self._safe_eval(expression)
            self.memory = result
            return result
        except ZeroDivisionError:
            return "Error: Division by zero!"
        except ValueError as e:
            return f"Error: Invalid value - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _safe_eval(self, expression: str) -> float:
        """
        Safe mathematical expression evaluation
        """
        # Only allow numbers, operators and parentheses
        allowed_chars = set('0123456789+-*/.()% ')
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Invalid character")
        
        
        allowed_names = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "pow": pow,
            "max": max,
            "min": min
        }
        
        return eval(expression, allowed_names)


def print_banner():
    """Prints the startup banner"""
    print("=" * 50)
    print("🧮  CLI CALCULATOR  🧮")
    print("=" * 50)
    print("Commands:")
    print("  • Math operations: +, -, *, /, **, %")
    print("  • Previous result: 'ans' or 'memory'")
    print("  • Clear memory: 'clear' or 'c'")
    print("  • Exit: 'quit', 'exit' or 'q'")
    print("=" * 50)
    print("Examples:")
    print("  > 2 + 3")
    print("  > ans * 4")
    print("  > (5 + 3) ** 2")
    print("=" * 50)


def main():
    """Main program loop"""
    calc = Calculator()
    print_banner()
    
    while True:
        try:
            expression = input("\n📱 Calculator > ").strip()
            
            if not expression:
                continue
            
            # Calculate
            result = calc.calculate(expression)
            
            if result == 'quit':
                print("\n👋 Goodbye!")
                break
            
            if isinstance(result, (int, float)):
                print(f"📊 Result: {result}")
                if result != int(result):
                    print(f"📊 Rounded: {round(result, 6)}")
            else:
                print(f"💬 {result}")
        
        except KeyboardInterrupt:
            print("\n\n👋 Exiting...")
            break
        except EOFError:
            print("\n\n👋 Exiting...")
            break


if __name__ == "__main__":
    main()