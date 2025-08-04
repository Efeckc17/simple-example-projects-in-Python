import tkinter as tk
from tkinter import ttk, messagebox
import random
import time


class NumberGuessingGameGUI:
    
    def __init__(self):
        # Create main window
        self.window = tk.Tk()
        self.setup_window()
        
        # Game configuration
        self.difficulty_levels = {
            'Easy': {'range': (1, 50), 'attempts': 10, 'color': '#28a745'},
            'Medium': {'range': (1, 100), 'attempts': 7, 'color': '#ffc107'},
            'Hard': {'range': (1, 200), 'attempts': 5, 'color': '#fd7e14'},
            'Expert': {'range': (1, 500), 'attempts': 8, 'color': '#dc3545'}
        }
        
        # Game state
        self.current_game = None
        self.game_stats = {
            'games_played': 0,
            'games_won': 0,
            'total_attempts': 0,
            'best_score': float('inf')
        }
        
        self.create_widgets()
    
    def setup_window(self):
        self.window.title("🎮 Number Guessing Game")
        self.window.resizable(True, True)
        self.window.minsize(500, 600)
        
        # Apply modern theme
        style = ttk.Style()
        style.theme_use('clam')
    
    def create_widgets(self):
        # Configure main window grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # Main container
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.create_header(main_frame)
        self.create_difficulty_selection(main_frame)
        self.create_game_area(main_frame)
        self.create_stats_area(main_frame)
        
        # Center window after widgets are created
        self.center_window()
    
    def center_window(self):
        # Update window to calculate size needed
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
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))
        
        title_label = tk.Label(
            header_frame,
            text="🎮 Number Guessing Game",
            font=("Segoe UI", 24, "bold"),
            fg="#2c3e50"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Can you guess the secret number?",
            font=("Segoe UI", 12),
            fg="#7f8c8d"
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_difficulty_selection(self, parent):
        difficulty_frame = ttk.LabelFrame(parent, text="Select Difficulty", padding="15")
        difficulty_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Difficulty selection variable
        self.selected_difficulty = tk.StringVar(value="Medium")
        
        row = 0
        for difficulty, config in self.difficulty_levels.items():
            range_text = f"Range: {config['range'][0]}-{config['range'][1]}"
            attempts_text = f"Attempts: {config['attempts']}"
            
            # Radio button for difficulty selection
            radio = ttk.Radiobutton(
                difficulty_frame,
                text=f"{difficulty}  |  {range_text}  |  {attempts_text}",
                variable=self.selected_difficulty,
                value=difficulty
            )
            radio.grid(row=row, column=0, sticky="w", pady=2)
            row += 1
        
        # Start game button
        start_btn = ttk.Button(
            difficulty_frame,
            text="🎲 Start New Game",
            command=self.start_new_game,
            style="Accent.TButton"
        )
        start_btn.grid(row=row, column=0, pady=(15, 0))
        
        difficulty_frame.columnconfigure(0, weight=1)
    
    def create_game_area(self, parent):
        # Game area container
        self.game_frame = ttk.LabelFrame(parent, text="Game Area", padding="15")
        self.game_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        
        # Game info display
        self.game_info_label = tk.Label(
            self.game_frame,
            text="Select difficulty and start a new game!",
            font=("Segoe UI", 11),
            fg="#6c757d",
            wraplength=400
        )
        self.game_info_label.pack(pady=(0, 15))
        
        # Input area
        input_frame = ttk.Frame(self.game_frame)
        input_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(input_frame, text="Your guess:").pack(side="left")
        
        # Entry for guess input
        self.guess_entry = ttk.Entry(input_frame, width=15, state="disabled")
        self.guess_entry.pack(side="left", padx=(10, 10))
        
        # Submit guess button
        self.submit_btn = ttk.Button(
            input_frame,
            text="🎯 Submit Guess",
            command=self.submit_guess,
            state="disabled"
        )
        self.submit_btn.pack(side="left")
        
        # Bind Enter key to submit
        self.guess_entry.bind('<Return>', lambda e: self.submit_guess())
        
        # Feedback area
        self.feedback_text = tk.Text(
            self.game_frame,
            height=8,
            width=50,
            font=("Consolas", 10),
            wrap="word",
            state="disabled"
        )
        
        # Scrollbar for feedback
        feedback_scrollbar = ttk.Scrollbar(self.game_frame, orient="vertical", command=self.feedback_text.yview)
        self.feedback_text.configure(yscrollcommand=feedback_scrollbar.set)
        
        self.feedback_text.pack(side="left", fill="both", expand=True)
        feedback_scrollbar.pack(side="right", fill="y")
        
        self.game_frame.columnconfigure(0, weight=1)
    
    def create_stats_area(self, parent):
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding="15")
        stats_frame.grid(row=3, column=0, sticky="ew")
        
        # Statistics display
        self.stats_text = tk.Text(
            stats_frame,
            height=6,
            font=("Segoe UI", 10),
            state="disabled",
            wrap="none"
        )
        self.stats_text.pack(fill="both", expand=True)
        
        # Buttons
        button_frame = ttk.Frame(stats_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        refresh_stats_btn = ttk.Button(
            button_frame,
            text="📊 Refresh Stats",
            command=self.update_stats_display
        )
        refresh_stats_btn.pack(side="left")
        
        instructions_btn = ttk.Button(
            button_frame,
            text="❓ How to Play",
            command=self.show_instructions
        )
        instructions_btn.pack(side="left", padx=(10, 0))
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)
        
        # Initialize stats display
        self.update_stats_display()
    
    def start_new_game(self):
        difficulty = self.selected_difficulty.get()
        config = self.difficulty_levels[difficulty]
        
        # Initialize game state
        self.current_game = {
            'difficulty': difficulty,
            'secret_number': random.randint(*config['range']),
            'attempts_used': 0,
            'max_attempts': config['attempts'],
            'range': config['range'],
            'start_time': time.time()
        }
        
        # Update UI
        self.guess_entry.config(state="normal")
        self.submit_btn.config(state="normal")
        self.guess_entry.focus()
        
        # Clear previous feedback
        self.clear_feedback()
        
        # Show game info
        range_text = f"{config['range'][0]}-{config['range'][1]}"
        info_text = (f"🎲 New {difficulty} game started!\n"
                    f"Range: {range_text} | Max attempts: {config['attempts']}\n"
                    f"Secret number generated... Good luck! 🍀")
        
        self.game_info_label.config(text=info_text, fg="#28a745")
        self.add_feedback("🎮 Game started! Enter your first guess below.", "#28a745")
    
    def submit_guess(self):
        # Check if game is active and controls are enabled
        if not self.current_game or self.submit_btn['state'] == 'disabled':
            return
        
        try:
            # Get and validate input
            guess_text = self.guess_entry.get().strip()
            if not guess_text:
                messagebox.showwarning("Input Error", "Please enter a number!")
                return
            
            guess = int(guess_text)
            game_range = self.current_game['range']
            
            if guess < game_range[0] or guess > game_range[1]:
                messagebox.showwarning(
                    "Invalid Range", 
                    f"Number must be between {game_range[0]} and {game_range[1]}!"
                )
                return
            
            # Process guess
            self.current_game['attempts_used'] += 1
            attempts_left = self.current_game['max_attempts'] - self.current_game['attempts_used']
            
            self.add_feedback(f"Attempt {self.current_game['attempts_used']}: You guessed {guess}")
            
            if guess == self.current_game['secret_number']:
                self.handle_win()
            elif self.current_game['attempts_used'] >= self.current_game['max_attempts']:
                self.handle_loss()
            else:
                # Provide hints
                if guess < self.current_game['secret_number']:
                    hint = self.get_hint(guess, self.current_game['secret_number'], game_range)
                    self.add_feedback(f"📈 Too low! {hint}", "#ff6b6b")
                else:
                    hint = self.get_hint(guess, self.current_game['secret_number'], game_range)
                    self.add_feedback(f"📉 Too high! {hint}", "#ff6b6b")
                
                # Temperature hints
                difference = abs(guess - self.current_game['secret_number'])
                if difference <= 5:
                    self.add_feedback("🔥 You're very close!", "#ff9500")
                elif difference <= 15:
                    self.add_feedback("🌡️ Getting warmer...", "#ffcc02")
                elif difference <= 30:
                    self.add_feedback("❄️ Getting colder...", "#74b9ff")
                
                self.add_feedback(f"📍 {attempts_left} attempts remaining\n", "#6c757d")
            
            # Clear input for next guess
            self.guess_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number!")
    
    def get_hint(self, guess, secret, game_range):
        # Calculate hint based on distance
        difference = abs(guess - secret)
        range_size = game_range[1] - game_range[0]
        
        if difference <= range_size * 0.05:
            return "🎯 Extremely close!"
        elif difference <= range_size * 0.1:
            return "🔥 Very close!"
        elif difference <= range_size * 0.2:
            return "🌡️ Close!"
        elif difference <= range_size * 0.4:
            return "❄️ Not so close..."
        else:
            return "🧊 Far away..."
    
    def handle_win(self):
        # Check if game is still active
        if not self.current_game:
            return
        
        # Store values before ending game
        attempts_used = self.current_game['attempts_used']
        elapsed_time = round(time.time() - self.current_game['start_time'], 1)
        max_attempts = self.current_game['max_attempts']
        
        # Update statistics
        self.game_stats['games_played'] += 1
        self.game_stats['games_won'] += 1
        self.game_stats['total_attempts'] += attempts_used
        
        if attempts_used < self.game_stats['best_score']:
            self.game_stats['best_score'] = attempts_used
        
        # Show win message
        self.add_feedback("\n🎉🎉🎉 CONGRATULATIONS! 🎉🎉🎉", "#28a745")
        self.add_feedback("🏆 YOU WON! 🏆", "#28a745")
        self.add_feedback(f"✅ Found in {attempts_used} attempts!", "#28a745")
        self.add_feedback(f"⏱️ Time: {elapsed_time} seconds", "#28a745")
        
        # Performance rating
        performance = (max_attempts - attempts_used + 1) / max_attempts
        if performance > 0.8:
            self.add_feedback("🌟 Performance: EXCELLENT!", "#ffd700")
        elif performance > 0.6:
            self.add_feedback("👍 Performance: GOOD!", "#28a745")
        elif performance > 0.4:
            self.add_feedback("👌 Performance: FAIR", "#ffc107")
        else:
            self.add_feedback("💪 Performance: Keep practicing!", "#6c757d")
        
        # End game first to prevent multiple calls
        self.end_game()
        self.update_stats_display()
        
        # Show win dialog
        messagebox.showinfo("Congratulations!", f"You won in {attempts_used} attempts!")
    
    def handle_loss(self):
        # Check if game is still active
        if not self.current_game:
            return
        
        # Store secret number before ending game
        secret_number = self.current_game['secret_number']
        
        # Update statistics
        self.game_stats['games_played'] += 1
        
        # Show loss message
        self.add_feedback("\n💀💀💀 GAME OVER! 💀💀💀", "#dc3545")
        self.add_feedback(f"😞 The secret number was: {secret_number}", "#dc3545")
        self.add_feedback("Better luck next time! 💪", "#6c757d")
        
        # End game first to prevent multiple calls
        self.end_game()
        self.update_stats_display()
        
        # Show loss dialog
        messagebox.showinfo("Game Over", f"The secret number was {secret_number}.\nBetter luck next time!")
    
    def end_game(self):
        # Disable game controls
        self.guess_entry.config(state="disabled")
        self.submit_btn.config(state="disabled")
        
        # Update game info
        self.game_info_label.config(
            text="Game finished! Select difficulty and start a new game.", 
            fg="#6c757d"
        )
        
        # Clear current game
        self.current_game = None
    
    def add_feedback(self, message, color="#000000"):
        # Add message to feedback area
        self.feedback_text.config(state="normal")
        self.feedback_text.insert(tk.END, message + "\n")
        
        # Apply color to the last line
        last_line_start = self.feedback_text.index("end-2l linestart")
        last_line_end = self.feedback_text.index("end-1c")
        
        # Create and apply tag for coloring
        tag_name = f"color_{len(message)}{time.time()}"
        self.feedback_text.tag_add(tag_name, last_line_start, last_line_end)
        self.feedback_text.tag_config(tag_name, foreground=color)
        
        # Scroll to bottom
        self.feedback_text.see(tk.END)
        self.feedback_text.config(state="disabled")
    
    def clear_feedback(self):
        # Clear feedback area
        self.feedback_text.config(state="normal")
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.config(state="disabled")
    
    def update_stats_display(self):
        # Update statistics display
        stats = self.game_stats
        
        if stats['games_played'] == 0:
            stats_text = "📊 No games played yet!\nStart a game to see your statistics."
        else:
            win_rate = (stats['games_won'] / stats['games_played']) * 100
            avg_attempts = stats['total_attempts'] / stats['games_won'] if stats['games_won'] > 0 else 0
            best_score = stats['best_score'] if stats['best_score'] != float('inf') else 'N/A'
            
            stats_text = f"""📊 GAME STATISTICS
🎮 Games played: {stats['games_played']}
🏆 Games won: {stats['games_won']}
📈 Win rate: {win_rate:.1f}%
🎯 Best score: {best_score} attempts
📊 Average attempts: {avg_attempts:.1f}"""
        
        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        self.stats_text.config(state="disabled")
    
    def show_instructions(self):
        # Show game instructions in dialog
        instructions = """🎯 HOW TO PLAY

📋 Rules:
• Choose a difficulty level
• Computer picks a random number in range
• You have limited attempts to guess
• Get hints after each wrong guess
• Win by finding the number!

🎨 Hint System:
• 📈/📉 Direction hints (higher/lower)
• 🔥❄️ Temperature hints (hot/cold)
• 🎯 Distance hints (close/far)

🏆 Difficulty Levels:
• EASY: 1-50, 10 attempts
• MEDIUM: 1-100, 7 attempts  
• HARD: 1-200, 5 attempts
• EXPERT: 1-500, 8 attempts

Good luck! 🍀"""
        
        messagebox.showinfo("How to Play", instructions)
    
    def run(self):
        # Start the application
        self.window.mainloop()


def main():
    try:
        # Create and run the application
        app = NumberGuessingGameGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")


if __name__ == "__main__":
    main()