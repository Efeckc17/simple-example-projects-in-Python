# 🐍 Simple Python Projects

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/Efeckc17/simple-example-projects-in-Python)
![Forks](https://img.shields.io/github/forks/Efeckc17/simple-example-projects-in-Python)
![Issues](https://img.shields.io/github/issues/Efeckc17/simple-example-projects-in-Python)
![Last Commit](https://img.shields.io/github/last-commit/Efeckc17/simple-example-projects-in-Python)

Collection of simple Python projects for learning and practice.

## 📋 Projects Overview

| Project | Technologies | Difficulty | Description | Jump to |
|---------|-------------|------------|-------------|---------|
| 🧮 **Calculator** | CLI, Tkinter, Flask, HTML/CSS/JS | ⭐⭐ Beginner | Multi-platform calculator with different interfaces | [Details](#-calculator) |
| 🔐 **Password Generator** | CLI, Tkinter, Clipboard API | ⭐⭐ Beginner | Secure password generation with customizable options | [Details](#-password-generator) |
| 🎮 **Number Guessing Game** | CLI, Tkinter, Game Logic | ⭐ Easy | Interactive guessing game with multiple difficulty levels | [Details](#-number-guessing-game) |
| 📝 **TODO App** | SQLite, CLI, Tkinter, CRUD | ⭐⭐⭐ Intermediate | Task management with database operations | [Details](#-todo-app-with-sqlite) |
| 🌐 **Speed Test** | Network API, Threading, Progress | ⭐⭐⭐ Intermediate | Internet speed testing with real-time updates | [Details](#-internet-speed-test) |
| 🎨 **ASCII Art Generator** | Image Processing, CLI, File I/O | ⭐⭐ Beginner | Convert text and images to ASCII art | [Details](#-ascii-art-generator) |
| 👤 **User Management API** | Flask API, JWT, SQLite, Full-Stack , HTML/CSS/JS  | ⭐⭐⭐⭐ Advanced | Complete API with authentication and frontend | [Details](#-user-management-api) |

## 📁 Project Details

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

### 📝 TODO App with SQLite
A task management application demonstrating SQLite database operations:

- **CLI** - Command line interface with comprehensive menu system
- **GUI** - Modern Tkinter interface with all CRUD operations

#### Features:
- **SQLite Database Integration** - Learn SQL operations hands-on
- **CRUD Operations** - Create, Read, Update, Delete tasks
- **Advanced Filtering** - View by status, search functionality
- **Priority System** - High, Medium, Low priority levels
- **Statistics Dashboard** - Task completion analytics
- **Database Management** - View database info and structure

#### SQL Concepts Demonstrated:
- **CREATE TABLE** - Database schema design
- **INSERT** - Adding new records
- **SELECT** - Querying data with WHERE, ORDER BY
- **UPDATE** - Modifying existing records
- **DELETE** - Removing records
- **AGGREGATION** - COUNT, GROUP BY for statistics
- **SEARCH** - LIKE operator for text search

#### Run the projects:
```bash
# CLI TODO App
cd todo-app/cli
python todo_cli.py

# GUI TODO App
cd todo-app/gui
python todo_gui.py

# Database demo (standalone)
cd todo-app
python database.py
```

### 🌐 Internet Speed Test
A network performance testing application using Speedtest.net:

- **CLI** - Command line interface with detailed progress and history
- **GUI** - Modern Tkinter interface with real-time updates

#### Features:
- **Download/Upload Speed Testing** - Accurate bandwidth measurement
- **Ping/Latency Testing** - Network responsiveness measurement
- **Real-time Progress** - Live updates during testing
- **Test History** - Save and view previous test results
- **Server Selection** - Choose specific test servers
- **Performance Analysis** - Detailed speed ratings and recommendations
- **Statistics Dashboard** - Historical data analysis

#### Network Concepts Demonstrated:
- **HTTP Requests** - Network communication protocols
- **Threading** - Background operations without blocking UI
- **Progress Callbacks** - Real-time status updates
- **JSON Storage** - Data persistence for test history
- **API Integration** - Using external services (Speedtest.net)

#### Run the projects:
```bash
# Install dependencies first
cd speedtest-app
pip install -r requirements.txt

# CLI Speed Test
cd cli
python speedtest_cli.py

# GUI Speed Test
cd ../gui
python speedtest_gui.py

# Core module demo
cd ..
python speedtest_core.py
```

### 🎨 ASCII Art Generator
A creative CLI tool for converting text and images to ASCII art:

- **Text to ASCII** - Transform text using various artistic fonts
- **Image to ASCII** - Convert images to character-based art

#### Features:
- **Multiple Font Styles** - 25+ figlet fonts (slant, big, block, bubble, etc.)
- **Character Set Options** - Detailed, simple, classic, minimal character sets
- **Image Processing** - Convert JPG, PNG, and other formats to ASCII
- **Customizable Output** - Adjustable width, border options
- **File Export** - Save ASCII art to text files
- **Preview Functions** - Preview fonts and character sets before converting

#### Text Conversion Examples:
- Basic: Simple text to ASCII art
- Styled: Custom fonts and decorative borders
- Sized: Adjustable width for different displays

#### Image Conversion Examples:
- Photos: Convert portraits and landscapes
- Logos: Transform brand graphics to text art
- Icons: Create ASCII versions of symbols

#### Run the project:
```bash
# Install dependencies
cd ascii-art-generator
pip install -r requirements.txt

# Convert text to ASCII art
python ascii_generator.py text "Hello World"
python ascii_generator.py text "Python" --font big --width 120

# Convert image to ASCII art
python ascii_generator.py image photo.jpg --width 100
python ascii_generator.py image logo.png --chars simple --banner

# Preview available options
python ascii_generator.py --list-fonts
python ascii_generator.py --list-chars
python ascii_generator.py --preview-fonts "ABC"

# Save to file
python ascii_generator.py text "Save Me" --output my_art.txt

# Get detailed help
python ascii_generator.py --help-detailed
```

### 👤 User Management API
A complete full-stack web application demonstrating modern API development:

- **Backend** - Flask API with JWT authentication and SQLite database
- **Frontend** - Modern vanilla JavaScript with responsive design

#### Features:
- **JWT Authentication** - Secure token-based login system
- **User Registration** - Account creation with validation
- **Profile Management** - Edit username, email, and avatar
- **Avatar Upload** - Image processing and storage
- **Admin Dashboard** - User statistics and activity logs
- **Server Logging** - Comprehensive activity tracking
- **Real-time Updates** - Live dashboard data

#### API Endpoints:
- **POST /api/register** - User registration
- **POST /api/login** - User authentication
- **GET /api/profile** - Get user profile
- **PUT /api/profile** - Update profile information
- **POST /api/upload-avatar** - Profile picture upload
- **GET /api/logs** - Server activity logs
- **GET /api/stats** - User statistics

#### Frontend Features:
- **Single Page Application** - No page reloads
- **Responsive Design** - Works on all devices
- **Modern UI/UX** - Clean, professional interface
- **Form Validation** - Client and server-side validation
- **File Upload** - Drag & drop avatar upload
- **Real-time Alerts** - User feedback system

#### Security Features:
- **Password Hashing** - bcrypt encryption
- **JWT Tokens** - Secure authentication
- **Input Validation** - SQL injection prevention
- **File Validation** - Safe image uploads
- **CORS Configuration** - Cross-origin protection

#### Run the project:
```bash
# Install dependencies
cd user-management-api
pip install -r requirements.txt

# Start backend server
cd backend
python app.py
# Backend: http://localhost:5000

# Start frontend (new terminal)
cd ../frontend
python -m http.server 3000
# Frontend: http://localhost:3000

# Test API with cURL
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"password123"}'
```

## 🛠️ Global Requirements

- **Python 3.7+** (Required for all projects)
- **Flask** - Web calculator, User management API
- **pyperclip** - GUI password generator clipboard features
- **speedtest-cli** - Internet speed test functionality
- **Pillow** - ASCII art generator image processing, User API avatar processing
- **pyfiglet** - ASCII art generator text styling
- **bcrypt** - User management API password hashing
- **PyJWT** - User management API authentication
- **Flask-CORS** - User management API cross-origin requests

### 📦 Quick Install All Dependencies
```bash
# Install all project dependencies at once
pip install flask pyperclip speedtest-cli Pillow pyfiglet bcrypt PyJWT Flask-CORS
```

## 🎯 Learning Goals

This repository demonstrates progressive Python concepts:

| Skill Level | Technologies Covered | Projects |
|-------------|---------------------|----------|
| **🟢 Beginner** | Basic Python, Input/Output, Conditionals | Calculator, Password Gen, Guessing Game, ASCII Art |
| **🟡 Intermediate** | GUI Programming, Database, File I/O | TODO App, Advanced GUIs |
| **🟠 Advanced** | Threading, API Integration, Network Programming | Speed Test, Web Calculator |
| **🔴 Expert** | Full-Stack Development, Authentication, Security | User Management API |

### 📚 Technical Concepts
- **Multiple Implementation Approaches** - Same functionality, different technologies
- **GUI Development** - Desktop applications with Tkinter
- **Web Development** - Full-stack applications with Flask
- **CLI Applications** - Command-line interfaces and argument parsing
- **Database Programming** - SQLite integration and SQL operations
- **Network Programming** - HTTP requests and API integration
- **Threading** - Background operations and real-time updates
- **CRUD Operations** - Create, Read, Update, Delete data patterns
- **API Development** - RESTful API design and implementation
- **Authentication & Security** - JWT tokens, password hashing, CORS
- **Frontend-Backend Integration** - Full-stack communication patterns
- **Code Organization** - Clean project structure and best practices
- **Security Practices** - Safe input handling and validation

## 🚀 Quick Start Guide

1. **Clone the repository**
   ```bash
   git clone https://github.com/Efeckc17/simple-example-projects-in-Python.git
   cd simple-example-projects-in-Python
   ```

2. **Install dependencies**
   ```bash
   pip install flask pyperclip speedtest-cli Pillow pyfiglet bcrypt PyJWT Flask-CORS
   ```

3. **Pick a project from the table above and follow the specific instructions!**

## 📄 License

MIT License

---

## 🌟 Support This Project

If you find this repository helpful for learning Python, please:

⭐ **Star the repository** - Show your support!  
🍴 **Fork it** - Create your own version  
🐛 **Report issues** - Help us improve  
💡 **Suggest features** - Share your ideas  

## 📞 Connect

- **GitHub:** [@Efeckc17](https://github.com/Efeckc17)
- **Repository:** [simple-example-projects-in-Python](https://github.com/Efeckc17/simple-example-projects-in-Python)

⭐ Star this repo if you find it useful for learning Python!