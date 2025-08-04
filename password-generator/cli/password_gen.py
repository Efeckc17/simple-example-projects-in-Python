"""
CLI Password Generator
Simple command-line password generator with customizable options
To see the commands and usage, run "python password_gen.py --help"
example usage: python password_gen.py -l 16 -c 3.
"""

import random
import string
import argparse
import sys


class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate(self, length=12, use_uppercase=True, use_digits=True, 
                 use_symbols=True, exclude_ambiguous=False):
        """Generate password with given parameters"""
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
        """Basic password strength check"""
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


def print_banner():
    print("=" * 50)
    print("🔐  PASSWORD GENERATOR  🔐")
    print("=" * 50)


def interactive_mode():
    """Interactive password generation"""
    gen = PasswordGenerator()
    
    while True:
        print("\n📝 Password Options:")
        
        try:
            length = int(input("Length (8-128, default 12): ") or "12")
            if not 8 <= length <= 128:
                print("❌ Length must be between 8 and 128")
                continue
        except ValueError:
            print("❌ Please enter a valid number")
            continue
        
        use_upper = input("Include uppercase? (Y/n): ").lower() != 'n'
        use_digits = input("Include numbers? (Y/n): ").lower() != 'n'
        use_symbols = input("Include symbols? (Y/n): ").lower() != 'n'
        exclude_ambiguous = input("Exclude ambiguous chars (0,O,1,l)? (y/N): ").lower() == 'y'
        
        try:
            count = int(input("How many passwords? (1-10, default 1): ") or "1")
            if not 1 <= count <= 10:
                print("❌ Count must be between 1 and 10")
                continue
        except ValueError:
            print("❌ Please enter a valid number")
            continue
        
        print(f"\n🔐 Generated Password{'s' if count > 1 else ''}:")
        print("-" * 50)
        
        for i in range(count):
            password = gen.generate(length, use_upper, use_digits, use_symbols, exclude_ambiguous)
            strength, feedback = gen.check_strength(password)
            
            print(f"{i+1}. {password}")
            print(f"   Strength: {strength}")
            if feedback:
                print(f"   Suggestions: {', '.join(feedback)}")
            print()
        
        again = input("Generate more passwords? (y/N): ").lower()
        if again != 'y':
            break


def main():
    parser = argparse.ArgumentParser(description="Generate secure passwords")
    parser.add_argument("-l", "--length", type=int, default=12, 
                       help="Password length (default: 12)")
    parser.add_argument("-c", "--count", type=int, default=1,
                       help="Number of passwords (default: 1)")
    parser.add_argument("--no-upper", action="store_true",
                       help="Exclude uppercase letters")
    parser.add_argument("--no-digits", action="store_true",
                       help="Exclude numbers")
    parser.add_argument("--no-symbols", action="store_true",
                       help="Exclude symbols")
    parser.add_argument("--exclude-ambiguous", action="store_true",
                       help="Exclude ambiguous characters (0,O,1,l)")
    parser.add_argument("-i", "--interactive", action="store_true",
                       help="Interactive mode")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.interactive:
        interactive_mode()
        return
    
    # Validate arguments
    if not 8 <= args.length <= 128:
        print("❌ Length must be between 8 and 128")
        sys.exit(1)
    
    if not 1 <= args.count <= 10:
        print("❌ Count must be between 1 and 10")
        sys.exit(1)
    
    gen = PasswordGenerator()
    
    print(f"\n🔐 Generated Password{'s' if args.count > 1 else ''}:")
    print("-" * 50)
    
    for i in range(args.count):
        try:
            password = gen.generate(
                length=args.length,
                use_uppercase=not args.no_upper,
                use_digits=not args.no_digits,
                use_symbols=not args.no_symbols,
                exclude_ambiguous=args.exclude_ambiguous
            )
            
            strength, feedback = gen.check_strength(password)
            
            print(f"{i+1}. {password}")
            print(f"   Strength: {strength}")
            if feedback:
                print(f"   Suggestions: {', '.join(feedback)}")
            print()
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)