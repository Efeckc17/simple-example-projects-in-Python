import random
import time
import sys


class NumberGuessingGame:
    
    def __init__(self):
        self.difficulty_levels = {
            'easy': {'range': (1, 50), 'attempts': 10},
            'medium': {'range': (1, 100), 'attempts': 7},
            'hard': {'range': (1, 200), 'attempts': 5},
            'expert': {'range': (1, 500), 'attempts': 8}
        }
        
        self.game_stats = {
            'games_played': 0,
            'games_won': 0,
            'total_attempts': 0,
            'best_score': float('inf')
        }
    
    def print_banner(self):
        print("=" * 60)
        print("🎮  NUMBER GUESSING GAME  🎮")
        print("=" * 60)
        print("Try to guess the secret number!")
        print("You'll get hints to help you find it.")
        print("=" * 60)
    
    def display_difficulty_menu(self):
        print("\n🎯 Choose Difficulty Level:")
        print("-" * 40)
        
        for level, config in self.difficulty_levels.items():
            range_str = f"{config['range'][0]}-{config['range'][1]}"
            print(f"{level.upper():<8} | Range: {range_str:<8} | Attempts: {config['attempts']}")
        
        print("-" * 40)
    
    def get_difficulty_choice(self):
        while True:
            self.display_difficulty_menu()
            choice = input("\nEnter difficulty (easy/medium/hard/expert): ").lower().strip()
            
            if choice in self.difficulty_levels:
                return choice
            elif choice in ['quit', 'exit', 'q']:
                return None
            else:
                print("❌ Invalid choice! Please try again.")
    
    def play_round(self, difficulty):
        config = self.difficulty_levels[difficulty]
        min_num, max_num = config['range']
        max_attempts = config['attempts']
        
        # Generate secret number
        secret_number = random.randint(min_num, max_num)
        attempts_used = 0
        start_time = time.time()
        
        print(f"\n🎲 New Game Started!")
        print(f"Difficulty: {difficulty.upper()}")
        print(f"Range: {min_num} - {max_num}")
        print(f"Maximum attempts: {max_attempts}")
        print(f"Secret number generated... Good luck! 🍀")
        print("-" * 50)
        
        while attempts_used < max_attempts:
            attempts_left = max_attempts - attempts_used
            
            try:
                print(f"\nAttempt {attempts_used + 1}/{max_attempts} (📍 {attempts_left} left)")
                guess = int(input(f"Enter your guess ({min_num}-{max_num}): "))
                
                if guess < min_num or guess > max_num:
                    print(f"⚠️  Number must be between {min_num} and {max_num}!")
                    continue
                
                attempts_used += 1
                
                if guess == secret_number:
                    # Player won!
                    elapsed_time = round(time.time() - start_time, 1)
                    self.handle_win(attempts_used, max_attempts, elapsed_time)
                    return True
                
                elif guess < secret_number:
                    hint = self.get_hint(guess, secret_number, min_num, max_num)
                    print(f"📈 Too low! {hint}")
                    
                else:
                    hint = self.get_hint(guess, secret_number, min_num, max_num)
                    print(f"📉 Too high! {hint}")
                
                # Additional hints based on closeness
                difference = abs(guess - secret_number)
                if difference <= 5:
                    print("🔥 You're very close!")
                elif difference <= 15:
                    print("🌡️  Getting warmer...")
                elif difference <= 30:
                    print("❄️  Getting colder...")
                
            except ValueError:
                print("❌ Please enter a valid number!")
            except KeyboardInterrupt:
                print("\n\n👋 Game interrupted. Goodbye!")
                return False
        
        # Player lost
        self.handle_loss(secret_number)
        return False
    
    def get_hint(self, guess, secret, min_range, max_range):
        difference = abs(guess - secret)
        range_size = max_range - min_range
        
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
    
    def handle_win(self, attempts, max_attempts, time_taken):
        self.game_stats['games_played'] += 1
        self.game_stats['games_won'] += 1
        self.game_stats['total_attempts'] += attempts
        
        if attempts < self.game_stats['best_score']:
            self.game_stats['best_score'] = attempts
        
        print("\n" + "🎉" * 20)
        print("🏆 CONGRATULATIONS! YOU WON! 🏆")
        print("🎉" * 20)
        print(f"✅ You found the number in {attempts} attempts!")
        print(f"⏱️  Time taken: {time_taken} seconds")
        
        # Performance rating
        performance = (max_attempts - attempts + 1) / max_attempts
        if performance > 0.8:
            print("🌟 Performance: EXCELLENT!")
        elif performance > 0.6:
            print("👍 Performance: GOOD!")
        elif performance > 0.4:
            print("👌 Performance: FAIR")
        else:
            print("💪 Performance: Keep practicing!")
    
    def handle_loss(self, secret_number):
        self.game_stats['games_played'] += 1
        
        print("\n" + "💀" * 20)
        print("😞 GAME OVER!")
        print("💀" * 20)
        print(f"The secret number was: {secret_number}")
        print("Better luck next time! 💪")
    
    def show_statistics(self):
        stats = self.game_stats
        
        if stats['games_played'] == 0:
            print("\n📊 No games played yet!")
            return
        
        win_rate = (stats['games_won'] / stats['games_played']) * 100
        avg_attempts = stats['total_attempts'] / stats['games_won'] if stats['games_won'] > 0 else 0
        
        print("\n📊 GAME STATISTICS")
        print("=" * 30)
        print(f"🎮 Games played: {stats['games_played']}")
        print(f"🏆 Games won: {stats['games_won']}")
        print(f"📈 Win rate: {win_rate:.1f}%")
        print(f"🎯 Best score: {stats['best_score'] if stats['best_score'] != float('inf') else 'N/A'} attempts")
        print(f"📊 Average attempts: {avg_attempts:.1f}")
        print("=" * 30)
    
    def main_menu(self):
        while True:
            print("\n🎮 MAIN MENU")
            print("-" * 20)
            print("1. 🎲 Play Game")
            print("2. 📊 View Statistics")
            print("3. ❓ How to Play")
            print("4. 🚪 Exit")
            print("-" * 20)
            
            choice = input("Select option (1-4): ").strip()
            
            if choice == '1':
                difficulty = self.get_difficulty_choice()
                if difficulty:
                    self.play_round(difficulty)
                    input("\nPress Enter to continue...")
                else:
                    break
            
            elif choice == '2':
                self.show_statistics()
                input("\nPress Enter to continue...")
            
            elif choice == '3':
                self.show_instructions()
                input("\nPress Enter to continue...")
            
            elif choice == '4':
                print("\n👋 Thanks for playing! Goodbye!")
                break
            
            else:
                print("❌ Invalid option! Please choose 1-4.")
    
    def show_instructions(self):
        print("\n❓ HOW TO PLAY")
        print("=" * 40)
        print("🎯 Goal: Guess the secret number!")
        print("\n📋 Rules:")
        print("• Choose a difficulty level")
        print("• Computer picks a random number in range")
        print("• You have limited attempts to guess")
        print("• Get hints after each wrong guess")
        print("• Win by finding the number!")
        print("\n🎨 Hint System:")
        print("• 📈/📉 Direction hints (higher/lower)")
        print("• 🔥❄️ Temperature hints (hot/cold)")
        print("• 🎯 Distance hints (close/far)")
        print("\n🏆 Difficulty Levels:")
        for level, config in self.difficulty_levels.items():
            range_str = f"{config['range'][0]}-{config['range'][1]}"
            print(f"• {level.upper()}: {range_str}, {config['attempts']} attempts")
        print("=" * 40)
    
    def run(self):
        try:
            self.print_banner()
            self.main_menu()
        except KeyboardInterrupt:
            print("\n\n👋 Game interrupted. Goodbye!")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please restart the game.")


def main():
    game = NumberGuessingGame()
    game.run()


if __name__ == "__main__":
    main()