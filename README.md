# 🐍 Simple Python Projects

Collection of simple Python projects for learning and practice.

## 📁 Projects

### 🧮 Calculator
A calculator implemented in three different ways:

- **CLI** - Command line interface
- **GUI** - Desktop app with Tkinter  
- **Web** - Flask web application

#### Run the projects:
```bash
# CLI Calculator
cd calculator/cli
python calculator.py

# GUI Calculator  
cd calculator/tkinter
python calculator_gui.py

# Web Calculator
cd calculator/web
pip install -r requirements.txt
python app.py
# Open: http://localhost:5000
```

### 🔐 Password Generator
A secure password generator implemented in two different ways:

- **CLI** - Command line interface with interactive mode
- **GUI** - Desktop app with Tkinter and modern interface

#### Features:
- Customizable password length (8-128 characters)
- Character type selection (uppercase, digits, symbols)
- Exclude ambiguous characters option
- Password strength analysis
- Multiple password generation
- Clipboard integration (GUI version)

#### Run the projects:
```bash
# CLI Password Generator
cd password-generator/cli
python password_gen.py

# Interactive mode
python password_gen.py -i

# GUI Password Generator
cd password-generator/gui
pip install -r requirements.txt
python password_gui.py
```

### 🎮 Number Guessing Game
A fun guessing game implemented in two different ways:

- **CLI** - Command line interface with interactive menu
- **GUI** - Desktop app with modern Tkinter interface

#### Features:
- Multiple difficulty levels (Easy, Medium, Hard, Expert)
- Smart hint system (direction, temperature, distance)
- Real-time performance tracking
- Game statistics and scoring
- Colorful feedback and emojis
- Time tracking and performance rating

#### Difficulty Levels:
- **Easy:** 1-50, 10 attempts
- **Medium:** 1-100, 7 attempts  
- **Hard:** 1-200, 5 attempts
- **Expert:** 1-500, 8 attempts

#### Run the projects:
```bash
# CLI Number Guessing Game
cd number-guessing-game/cli
python number_game.py

# GUI Number Guessing Game
cd number-guessing-game/gui
python number_game_gui.py
```

## 🛠️ Requirements

- Python 3.7+
- Flask (for web calculator)
- pyperclip (for GUI password generator clipboard functionality)

## 🎯 Learning Goals

This repository demonstrates:
- **Multiple Implementation Approaches** - Same functionality with different technologies
- **GUI Development** - Desktop applications with Tkinter
- **Web Development** - Full-stack applications with Flask
- **CLI Applications** - Command-line interfaces and argument parsing
- **Code Organization** - Clean project structure and best practices
- **Security Practices** - Safe input handling and validation

## 📄 License

MIT License

---

⭐ Star this repo if you find it useful for learning Python!