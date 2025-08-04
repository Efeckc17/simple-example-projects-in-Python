import sys
import os
import time
import json
from datetime import datetime

# Add parent directory to path to import core module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from speedtest_core import SpeedTestCore


class SpeedTestCLI:
    
    def __init__(self):
        # Initialize core speedtest module
        self.speed_test = SpeedTestCore()
        
        # Set up history file path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.history_file = os.path.join(script_dir, "speedtest_history.json")
        
        # Load test history
        self.test_history = self.load_history()
        
        print("🌐 Internet Speed Test CLI")
        print("💾 Powered by Speedtest.net")
    
    def print_banner(self):
        """Print application banner"""
        print("\n" + "=" * 60)
        print("🌐  INTERNET SPEED TEST CLI  🌐")
        print("💾  Network Performance Testing Tool")
        print("=" * 60)
    
    def show_main_menu(self):
        """Display main menu options"""
        print("\n🚀 MAIN MENU")
        print("-" * 30)
        print("1. 🧪 Run Speed Test")
        print("2. 📊 View Test History")
        print("3. 📡 Server Information")
        print("4. 🎯 Test Specific Server")
        print("5. 📈 Compare Recent Tests")
        print("6. 🗑️ Clear History")
        print("7. ❓ Help & Information")
        print("0. 🚪 Exit")
        print("-" * 30)
    
    def progress_callback(self, progress: float, message: str):
        """Callback for progress updates"""
        # Create progress bar
        bar_length = 40
        filled_length = int(bar_length * progress // 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        print(f"\r[{bar}] {progress:.1f}% - {message}", end='', flush=True)
    
    def status_callback(self, status: str):
        """Callback for status updates"""
        print(f"\n{status}")
    
    def run_speed_test(self):
        """Run a complete speed test"""
        print("\n🧪 RUNNING SPEED TEST")
        print("-" * 25)
        print("⚠️  This may take 30-60 seconds...")
        print("📱 Please close other applications using internet")
        
        confirm = input("\nProceed with test? (Y/n): ").lower()
        if confirm == 'n':
            print("❌ Test cancelled!")
            return
        
        print("\n🚀 Starting speed test...")
        
        # Set up callbacks
        self.speed_test.set_callbacks(self.progress_callback, self.status_callback)
        
        # Run the test
        start_time = time.time()
        results = self.speed_test.run_full_test()
        end_time = time.time()
        
        if results:
            # Display results
            self.display_results(results)
            
            # Save to history
            self.save_test_result(results)
            
            print(f"\n⏱️ Total test time: {end_time - start_time:.1f} seconds")
        else:
            print("\n❌ Speed test failed! Please check your internet connection.")
    
    def display_results(self, results: dict):
        """Display speed test results in a formatted way"""
        print("\n\n" + "🎉" * 20)
        print("📊 SPEED TEST RESULTS")
        print("🎉" * 20)
        
        # Main results
        download = results.get('download_mbps', 0)
        upload = results.get('upload_mbps', 0)
        ping = results.get('ping_ms', 0)
        
        print(f"\n📥 Download Speed: {self.speed_test.format_speed(download)}")
        print(f"📤 Upload Speed:   {self.speed_test.format_speed(upload)}")
        print(f"🏓 Ping:           {ping:.2f} ms")
        
        # Rating
        rating = self.speed_test.get_speed_rating(download)
        print(f"⭐ Speed Rating:   {rating}")
        
        # Server info
        print(f"\n🎯 Test Server:")
        print(f"   📍 Location: {results.get('server_location', 'Unknown')}")
        print(f"   🌐 Host: {results.get('server_host', 'Unknown')}")
        
        # ISP info
        print(f"\n🌐 Your ISP: {results.get('isp', 'Unknown')}")
        
        # Timestamp
        print(f"🕒 Test Time: {results.get('timestamp', 'Unknown')}")
        
        # Performance analysis
        self.analyze_performance(download, upload, ping)
    
    def analyze_performance(self, download: float, upload: float, ping: float):
        """Analyze and provide feedback on performance"""
        print(f"\n📈 PERFORMANCE ANALYSIS")
        print("-" * 25)
        
        # Download analysis
        if download >= 100:
            print("📥 Download: Perfect for 4K streaming, large file downloads")
        elif download >= 50:
            print("📥 Download: Great for HD streaming, video calls")
        elif download >= 25:
            print("📥 Download: Good for regular streaming, web browsing")
        elif download >= 10:
            print("📥 Download: Suitable for basic web browsing, email")
        else:
            print("📥 Download: May struggle with video streaming")
        
        # Upload analysis
        if upload >= 10:
            print("📤 Upload: Excellent for video calls, file uploads")
        elif upload >= 5:
            print("📤 Upload: Good for video calls, cloud backup")
        elif upload >= 1:
            print("📤 Upload: Basic video calls, email attachments")
        else:
            print("📤 Upload: Limited for video calls, slow uploads")
        
        # Ping analysis
        if ping <= 20:
            print("🏓 Ping: Excellent for gaming, video calls")
        elif ping <= 50:
            print("🏓 Ping: Good for most online activities")
        elif ping <= 100:
            print("🏓 Ping: Acceptable for general use")
        else:
            print("🏓 Ping: May cause delays in real-time applications")
    
    def view_history(self):
        """Display test history"""
        print("\n📊 TEST HISTORY")
        print("-" * 15)
        
        if not self.test_history:
            print("📭 No test history available!")
            return
        
        print(f"📋 Total tests: {len(self.test_history)}")
        print(f"📅 Showing last 10 tests:\n")
        
        # Show last 10 tests
        recent_tests = self.test_history[-10:]
        
        for i, test in enumerate(reversed(recent_tests), 1):
            download = test.get('download_mbps', 0)
            upload = test.get('upload_mbps', 0)
            ping = test.get('ping_ms', 0)
            timestamp = test.get('timestamp', 'Unknown')
            
            print(f"{i:2d}. {timestamp}")
            print(f"    📥 {self.speed_test.format_speed(download):<12} "
                  f"📤 {self.speed_test.format_speed(upload):<12} "
                  f"🏓 {ping:.1f}ms")
        
        # Calculate averages
        if len(self.test_history) > 1:
            self.show_statistics()
    
    def show_statistics(self):
        """Show statistics from test history"""
        print(f"\n📈 STATISTICS")
        print("-" * 15)
        
        downloads = [t.get('download_mbps', 0) for t in self.test_history]
        uploads = [t.get('upload_mbps', 0) for t in self.test_history]
        pings = [t.get('ping_ms', 0) for t in self.test_history if t.get('ping_ms', 0) > 0]
        
        if downloads:
            avg_download = sum(downloads) / len(downloads)
            max_download = max(downloads)
            min_download = min(downloads)
            
            print(f"📥 Download - Avg: {self.speed_test.format_speed(avg_download)}, "
                  f"Max: {self.speed_test.format_speed(max_download)}, "
                  f"Min: {self.speed_test.format_speed(min_download)}")
        
        if uploads:
            avg_upload = sum(uploads) / len(uploads)
            max_upload = max(uploads)
            min_upload = min(uploads)
            
            print(f"📤 Upload   - Avg: {self.speed_test.format_speed(avg_upload)}, "
                  f"Max: {self.speed_test.format_speed(max_upload)}, "
                  f"Min: {self.speed_test.format_speed(min_upload)}")
        
        if pings:
            avg_ping = sum(pings) / len(pings)
            max_ping = max(pings)
            min_ping = min(pings)
            
            print(f"🏓 Ping     - Avg: {avg_ping:.1f}ms, "
                  f"Max: {max_ping:.1f}ms, "
                  f"Min: {min_ping:.1f}ms")
    
    def show_server_info(self):
        """Show available server information"""
        print("\n📡 SERVER INFORMATION")
        print("-" * 20)
        print("⏳ Getting server list...")
        
        server_info = self.speed_test.get_server_info()
        
        if 'error' in server_info:
            print(f"❌ Error getting servers: {server_info['error']}")
            return
        
        servers = server_info.get('servers', [])
        if not servers:
            print("❌ No servers found!")
            return
        
        print(f"🌐 Available servers (showing top {len(servers)}):\n")
        
        for i, server in enumerate(servers, 1):
            print(f"{i:2d}. {server['name']}, {server['country']}")
            print(f"    🌐 Host: {server['host']}")
            print(f"    📏 Distance: {server['distance']:.1f} km")
            print(f"    🆔 ID: {server['id']}")
            print()
    
    def test_specific_server(self):
        """Test with a specific server"""
        print("\n🎯 TEST SPECIFIC SERVER")
        print("-" * 22)
        
        server_id = input("Enter server ID: ").strip()
        
        if not server_id:
            print("❌ Invalid server ID!")
            return
        
        print(f"\n🧪 Testing with server ID: {server_id}")
        
        # Set up callbacks
        self.speed_test.set_callbacks(self.progress_callback, self.status_callback)
        
        # Run test with specific server
        results = self.speed_test.test_specific_server(server_id)
        
        if results:
            self.display_results(results)
            self.save_test_result(results)
        else:
            print("❌ Test with specific server failed!")
    
    def compare_recent_tests(self):
        """Compare recent test results"""
        print("\n📈 COMPARE RECENT TESTS")
        print("-" * 25)
        
        if len(self.test_history) < 2:
            print("❌ Need at least 2 tests for comparison!")
            return
        
        # Get last 2 tests
        latest = self.test_history[-1]
        previous = self.test_history[-2]
        
        print("📊 Latest vs Previous Test:")
        print("-" * 30)
        
        # Compare download
        latest_dl = latest.get('download_mbps', 0)
        previous_dl = previous.get('download_mbps', 0)
        dl_diff = latest_dl - previous_dl
        dl_percent = (dl_diff / previous_dl * 100) if previous_dl > 0 else 0
        
        print(f"📥 Download:")
        print(f"   Latest:   {self.speed_test.format_speed(latest_dl)}")
        print(f"   Previous: {self.speed_test.format_speed(previous_dl)}")
        print(f"   Change:   {dl_diff:+.2f} Mbps ({dl_percent:+.1f}%)")
        
        # Compare upload
        latest_ul = latest.get('upload_mbps', 0)
        previous_ul = previous.get('upload_mbps', 0)
        ul_diff = latest_ul - previous_ul
        ul_percent = (ul_diff / previous_ul * 100) if previous_ul > 0 else 0
        
        print(f"\n📤 Upload:")
        print(f"   Latest:   {self.speed_test.format_speed(latest_ul)}")
        print(f"   Previous: {self.speed_test.format_speed(previous_ul)}")
        print(f"   Change:   {ul_diff:+.2f} Mbps ({ul_percent:+.1f}%)")
        
        # Compare ping
        latest_ping = latest.get('ping_ms', 0)
        previous_ping = previous.get('ping_ms', 0)
        ping_diff = latest_ping - previous_ping
        
        print(f"\n🏓 Ping:")
        print(f"   Latest:   {latest_ping:.2f} ms")
        print(f"   Previous: {previous_ping:.2f} ms")
        print(f"   Change:   {ping_diff:+.2f} ms")
    
    def clear_history(self):
        """Clear test history"""
        print("\n🗑️ CLEAR HISTORY")
        print("-" * 15)
        
        if not self.test_history:
            print("📭 No history to clear!")
            return
        
        print(f"📋 Current history: {len(self.test_history)} tests")
        confirm = input("⚠️ Are you sure you want to clear all history? (y/N): ").lower()
        
        if confirm == 'y':
            self.test_history = []
            self.save_history()
            print("✅ History cleared!")
        else:
            print("❌ Operation cancelled!")
    
    def show_help(self):
        """Show help information"""
        print("\n❓ HELP & INFORMATION")
        print("-" * 22)
        print("🌐 About Internet Speed Tests:")
        print("   • Download: How fast you can receive data")
        print("   • Upload: How fast you can send data")
        print("   • Ping: Time for data to travel to server and back")
        print()
        print("📊 Speed Guidelines:")
        print("   • 1-5 Mbps: Basic web browsing, email")
        print("   • 5-25 Mbps: HD video streaming")
        print("   • 25-50 Mbps: Multiple devices, 4K streaming")
        print("   • 50+ Mbps: Gaming, large file downloads")
        print()
        print("🏓 Ping Guidelines:")
        print("   • <20ms: Excellent for gaming")
        print("   • 20-50ms: Good for most activities")
        print("   • 50-100ms: Acceptable")
        print("   • >100ms: May cause noticeable delays")
        print()
        print("💡 Tips for Better Results:")
        print("   • Close other applications using internet")
        print("   • Use wired connection if possible")
        print("   • Test multiple times for accuracy")
        print("   • Test at different times of day")
    
    def load_history(self) -> list:
        """Load test history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"⚠️ Error loading history: {e}")
            return []
    
    def save_history(self):
        """Save test history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.test_history, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving history: {e}")
    
    def save_test_result(self, results: dict):
        """Save a test result to history"""
        self.test_history.append(results)
        # Keep only last 50 tests
        self.test_history = self.test_history[-50:]
        self.save_history()
    
    def run(self):
        """Main application loop"""
        try:
            self.print_banner()
            
            while True:
                self.show_main_menu()
                
                choice = input("\nSelect option (0-7): ").strip()
                
                if choice == "0":
                    print("\n👋 Thank you for using Speed Test CLI!")
                    print("📊 All test results saved to history")
                    break
                
                elif choice == "1":
                    self.run_speed_test()
                
                elif choice == "2":
                    self.view_history()
                
                elif choice == "3":
                    self.show_server_info()
                
                elif choice == "4":
                    self.test_specific_server()
                
                elif choice == "5":
                    self.compare_recent_tests()
                
                elif choice == "6":
                    self.clear_history()
                
                elif choice == "7":
                    self.show_help()
                
                else:
                    print("❌ Invalid choice! Please select 0-7.")
                
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Application interrupted. Goodbye!")
        
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please restart the application.")


def main():
    """Main function"""
    app = SpeedTestCLI()
    app.run()


if __name__ == "__main__":
    main()