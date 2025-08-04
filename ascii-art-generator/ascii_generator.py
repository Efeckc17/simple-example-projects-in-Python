# Simple text conversion
# python ascii_generator.py text "Test"

# Font list 
# python ascii_generator.py --list-fonts

# Help
# python ascii_generator.py --help-detailed

import os
import sys
import argparse
from PIL import Image
import pyfiglet
from typing import Optional, List


class ASCIIArtGenerator:
    
    def __init__(self):
        # ASCII characters from darkest to lightest
        self.ascii_chars = "@%#*+=-:. "
        # Alternative character sets
        self.char_sets = {
            'detailed': "@%#*+=-:. ",
            'simple': "█▉▊▋▌▍▎▏ ",
            'classic': "#*+=-:. ",
            'minimal': "█░ "
        }
        
        # Available figlet fonts
        self.text_fonts = [
            'slant', 'big', 'block', 'bubble', 'digital', 'isometric1',
            'letters', 'alligator', 'banner', 'doom', 'epic', 'ghost',
            'graffiti', 'hollywood', 'invita', 'lean', 'mini', 'script',
            'shadow', 'small', 'smscript', 'speed', 'starwars', 'stop',
            'thick', 'thin', 'univers'
        ]
    
    def text_to_ascii(self, text: str, font: str = 'slant', width: int = 80) -> str:
        """Convert text to ASCII art using figlet"""
        try:
            # Check if font is available
            if font not in self.text_fonts:
                print(f"⚠️ Font '{font}' not available. Using 'slant' instead.")
                font = 'slant'
            
            # Generate ASCII art
            ascii_art = pyfiglet.figlet_format(text, font=font, width=width)
            return ascii_art
            
        except Exception as e:
            return f"❌ Error generating text ASCII: {str(e)}"
    
    def image_to_ascii(self, image_path: str, width: int = 80, 
                      char_set: str = 'detailed') -> str:
        """Convert image to ASCII art"""
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                return f"❌ Image file not found: {image_path}"
            
            # Get character set
            chars = self.char_sets.get(char_set, self.char_sets['detailed'])
            
            # Open and process image
            with Image.open(image_path) as img:
                # Convert to grayscale
                img = img.convert('L')
                
                # Calculate new dimensions
                aspect_ratio = img.height / img.width
                # ASCII characters are roughly twice as tall as wide
                height = int(width * aspect_ratio * 0.5)
                
                # Resize image
                img = img.resize((width, height))
                
                # Convert to ASCII
                ascii_lines = []
                for y in range(height):
                    line = ""
                    for x in range(width):
                        # Get pixel brightness (0-255)
                        pixel = img.getpixel((x, y))
                        # Map brightness to character index
                        char_index = int(pixel / 255 * (len(chars) - 1))
                        line += chars[char_index]
                    ascii_lines.append(line)
                
                return "\n".join(ascii_lines)
                
        except Exception as e:
            return f"❌ Error processing image: {str(e)}"
    
    def get_available_fonts(self) -> List[str]:
        """Get list of available figlet fonts"""
        return self.text_fonts
    
    def get_available_char_sets(self) -> List[str]:
        """Get list of available character sets"""
        return list(self.char_sets.keys())
    
    def preview_char_sets(self) -> str:
        """Show preview of all character sets"""
        preview = "🎨 Character Set Previews:\n"
        preview += "-" * 30 + "\n"
        
        for name, chars in self.char_sets.items():
            preview += f"{name:>10}: {chars}\n"
        
        return preview
    
    def preview_fonts(self, sample_text: str = "ABC") -> str:
        """Show preview of available fonts"""
        preview = "🔤 Font Previews:\n"
        preview += "=" * 40 + "\n"
        
        # Show first few fonts as examples
        sample_fonts = self.text_fonts[:8]
        
        for font in sample_fonts:
            try:
                ascii_text = pyfiglet.figlet_format(sample_text, font=font, width=60)
                preview += f"\n--- {font.upper()} ---\n"
                preview += ascii_text
            except:
                preview += f"\n--- {font.upper()} (Error) ---\n"
        
        preview += f"\n💡 Total available fonts: {len(self.text_fonts)}\n"
        preview += "Use --list-fonts to see all font names.\n"
        
        return preview
    
    def create_banner(self, text: str, char: str = "=", width: int = 60) -> str:
        """Create a decorative banner around text"""
        lines = text.split('\n')
        max_length = max(len(line) for line in lines) if lines else 0
        
        # Ensure width is at least as wide as the content
        if width < max_length + 4:
            width = max_length + 4
        
        # Top border
        banner = char * width + "\n"
        
        # Content with padding
        for line in lines:
            padding = (width - len(line) - 2) // 2
            banner += char + " " * padding + line + " " * (width - len(line) - padding - 2) + char + "\n"
        
        # Bottom border
        banner += char * width
        
        return banner
    
    def save_to_file(self, content: str, filename: str) -> bool:
        """Save ASCII art to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return False


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🎨  ASCII ART GENERATOR  🎨")
    print("Convert text and images to ASCII art")
    print("=" * 60)


def show_help():
    """Show detailed help information"""
    help_text = """
🎨 ASCII ART GENERATOR HELP

📝 TEXT TO ASCII:
  python ascii_generator.py text "Hello World"
  python ascii_generator.py text "Python" --font big
  python ascii_generator.py text "Code" --width 100

🖼️ IMAGE TO ASCII:
  python ascii_generator.py image photo.jpg
  python ascii_generator.py image logo.png --width 120
  python ascii_generator.py image pic.jpg --chars simple

📋 OPTIONS:
  --font FONT       Font for text (default: slant)
  --width WIDTH     Output width (default: 80)
  --chars CHARSET   Character set for images (detailed/simple/classic/minimal)
  --output FILE     Save to file instead of printing
  --banner          Add decorative border
  --list-fonts      Show available fonts
  --list-chars      Show character set previews
  --preview-fonts   Show font previews

💡 EXAMPLES:
  # Simple text conversion
  python ascii_generator.py text "ASCII Art"
  
  # Large text with specific font
  python ascii_generator.py text "BIG TEXT" --font big --width 120
  
  # Convert image with custom settings
  python ascii_generator.py image photo.jpg --width 100 --chars classic
  
  # Save output to file
  python ascii_generator.py text "Save Me" --output my_art.txt
  
  # Create bordered output
  python ascii_generator.py text "Bordered" --banner

🎯 TIPS:
  • Use simple character sets for better readability
  • Adjust width based on your terminal/output needs
  • Try different fonts to find the best style
  • Images work best with high contrast
  • Save complex art to files for sharing
"""
    print(help_text)


def main():
    """Main application function"""
    parser = argparse.ArgumentParser(
        description="🎨 ASCII Art Generator - Convert text and images to ASCII art",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Text command
    text_parser = subparsers.add_parser('text', help='Convert text to ASCII art')
    text_parser.add_argument('text', help='Text to convert')
    text_parser.add_argument('--font', default='slant', help='Font to use (default: slant)')
    text_parser.add_argument('--width', type=int, default=80, help='Output width (default: 80)')
    
    # Image command
    image_parser = subparsers.add_parser('image', help='Convert image to ASCII art')
    image_parser.add_argument('image_path', help='Path to image file')
    image_parser.add_argument('--width', type=int, default=80, help='Output width (default: 80)')
    image_parser.add_argument('--chars', default='detailed', help='Character set (default: detailed)')
    
    # Common options
    for subparser in [text_parser, image_parser]:
        subparser.add_argument('--output', help='Save to file instead of printing')
        subparser.add_argument('--banner', action='store_true', help='Add decorative border')
    
    # Info commands
    parser.add_argument('--list-fonts', action='store_true', help='List available fonts')
    parser.add_argument('--list-chars', action='store_true', help='Show character set previews')
    parser.add_argument('--preview-fonts', help='Preview fonts with sample text')
    parser.add_argument('--help-detailed', action='store_true', help='Show detailed help')
    
    args = parser.parse_args()
    
    # Create generator instance
    generator = ASCIIArtGenerator()
    
    # Handle info commands
    if args.list_fonts:
        print("🔤 Available Fonts:")
        fonts = generator.get_available_fonts()
        for i, font in enumerate(fonts, 1):
            print(f"{i:2d}. {font}")
        return
    
    if args.list_chars:
        print(generator.preview_char_sets())
        return
    
    if args.preview_fonts:
        sample = args.preview_fonts if args.preview_fonts != True else "ABC"
        print(generator.preview_fonts(sample))
        return
    
    if args.help_detailed:
        show_help()
        return
    
    # Handle main commands
    if not args.command:
        print_banner()
        print("\n🚀 Quick Start:")
        print("  python ascii_generator.py text \"Hello World\"")
        print("  python ascii_generator.py image photo.jpg")
        print("\n📖 For detailed help: python ascii_generator.py --help-detailed")
        return
    
    print_banner()
    
    # Process commands
    result = ""
    
    if args.command == 'text':
        print(f"🔤 Converting text: '{args.text}'")
        print(f"📝 Font: {args.font}, Width: {args.width}")
        result = generator.text_to_ascii(args.text, args.font, args.width)
    
    elif args.command == 'image':
        print(f"🖼️ Converting image: '{args.image_path}'")
        print(f"📐 Width: {args.width}, Character set: {args.chars}")
        result = generator.image_to_ascii(args.image_path, args.width, args.chars)
    
    # Add banner if requested
    if args.banner and result and not result.startswith('❌'):
        result = generator.create_banner(result)
    
    # Output result
    if args.output:
        if generator.save_to_file(result, args.output):
            print(f"💾 ASCII art saved to: {args.output}")
        else:
            print("❌ Failed to save file!")
    else:
        print(f"\n🎨 Result:")
        print("-" * 50)
        print(result)
        print("-" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ASCII Art Generator interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Use --help-detailed for usage information.")