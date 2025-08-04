#!/usr/bin/env python3
"""
Flask Web Calculator - Web-Based Calculator
===========================================

Modern and responsive web calculator
Developed with Flask, HTML, CSS and JavaScript
"""

from flask import Flask, render_template, request, jsonify
import operator
import math
from typing import Union, Dict, Any


app = Flask(__name__)
app.secret_key = 'calculator_secret_key_30'


class WebCalculator:
    """Web calculator backend class"""
    
    def __init__(self):
        self.operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '**': operator.pow,
            '%': operator.mod
        }
    
    def calculate(self, expression: str) -> Dict[str, Any]:
       
        try:
            if not self._is_safe_expression(expression):
                return {
                    'success': False,
                    'error': 'Invalid expression',
                    'result': None
                }
            
            result = self._safe_eval(expression)
            
            return {
                'success': True,
                'result': result,
                'error': None
            }
            
        except ZeroDivisionError:
            return {
                'success': False,
                'error': 'Division by zero error',
                'result': None
            }
        except ValueError as e:
            return {
                'success': False,
                'error': f'Value error: {str(e)}',
                'result': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Calculation error: {str(e)}',
                'result': None
            }
    
    def _is_safe_expression(self, expression: str) -> bool:
        """Checks if the expression is safe"""
        allowed_chars = set('0123456789+-*/.()% ')
        return all(c in allowed_chars for c in expression)
    
    def _safe_eval(self, expression: str) -> float:
        """Safe expression evaluation"""
        safe_dict = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "pow": pow,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "pi": math.pi,
            "e": math.e
        }
        
        return eval(expression, safe_dict)
    
    def advanced_function(self, func_name: str, value: float) -> Dict[str, Any]:
        try:
            if func_name == 'sqrt':
                if value < 0:
                    raise ValueError("Cannot calculate square root of negative number")
                result = math.sqrt(value)
            
            elif func_name == 'square':
                result = value ** 2
            
            elif func_name == 'reciprocal':
                if value == 0:
                    raise ZeroDivisionError("Cannot calculate reciprocal of zero")
                result = 1 / value
            
            elif func_name == 'factorial':
                if value < 0 or value != int(value):
                    raise ValueError("Factorial can only be calculated for positive integers")
                result = math.factorial(int(value))
            
            elif func_name == 'sin':
                result = math.sin(math.radians(value))
            
            elif func_name == 'cos':
                result = math.cos(math.radians(value))
            
            elif func_name == 'tan':
                result = math.tan(math.radians(value))
            
            elif func_name == 'log':
                if value <= 0:
                    raise ValueError("Logarithm can only be calculated for positive numbers")
                result = math.log10(value)
            
            elif func_name == 'ln':
                if value <= 0:
                    raise ValueError("Natural logarithm can only be calculated for positive numbers")
                result = math.log(value)
            
            else:
                raise ValueError(f"Unknown function: {func_name}")
            
            return {
                'success': True,
                'result': result,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'result': None
            }


# Global calculator instance
calculator = WebCalculator()


@app.route('/')
def index():
    """Main page"""
    return render_template('calculator.html')


@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """Calculation API endpoint"""
    data = request.get_json()
    
    if not data or 'expression' not in data:
        return jsonify({
            'success': False,
            'error': 'Expression required',
            'result': None
        }), 400
    
    expression = data['expression'].strip()
    result = calculator.calculate(expression)
    
    return jsonify(result)


@app.route('/api/function', methods=['POST'])
def api_function():
    """Advanced function API endpoint"""
    data = request.get_json()
    
    if not data or 'function' not in data or 'value' not in data:
        return jsonify({
            'success': False,
            'error': 'Function and value required',
            'result': None
        }), 400
    
    func_name = data['function']
    value = float(data['value'])
    
    result = calculator.advanced_function(func_name, value)
    return jsonify(result)


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'calculator'})


if __name__ == '__main__':
    print("🌐 Starting Web Calculator...")
    print("🔗 URL: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop")
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)