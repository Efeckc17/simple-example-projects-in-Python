import speedtest
import threading
import time
from datetime import datetime
from typing import Dict, Optional, Callable


class SpeedTestCore:
    
    def __init__(self):
        # Initialize speedtest client
        self.st = None
        self.results = {}
        self.is_testing = False
        
        # Callback functions for progress updates
        self.progress_callback = None
        self.status_callback = None
    
    def set_callbacks(self, progress_callback: Optional[Callable] = None, 
                     status_callback: Optional[Callable] = None):
        """Set callback functions for progress and status updates"""
        self.progress_callback = progress_callback
        self.status_callback = status_callback
    
    def _update_progress(self, progress: float, message: str = ""):
        """Internal method to update progress"""
        if self.progress_callback:
            self.progress_callback(progress, message)
    
    def _update_status(self, status: str):
        """Internal method to update status"""
        if self.status_callback:
            self.status_callback(status)
    
    def initialize_test(self) -> bool:
        """Initialize speedtest client and get server list"""
        try:
            self._update_status("🌐 Initializing speedtest...")
            self._update_progress(10, "Creating speedtest client...")
            
            # Create speedtest client
            self.st = speedtest.Speedtest()
            
            self._update_progress(30, "Getting server list...")
            self._update_status("📡 Getting best server...")
            
            # Get list of servers and select best one
            self.st.get_servers()
            self.st.get_best_server()
            
            self._update_progress(50, "Server selected")
            self._update_status(f"🎯 Connected to: {self.st.best['host']} ({self.st.best['country']})")
            
            return True
            
        except Exception as e:
            self._update_status(f"❌ Initialization failed: {str(e)}")
            return False
    
    def test_download(self) -> float:
        """Test download speed"""
        try:
            self._update_status("📥 Testing download speed...")
            self._update_progress(60, "Starting download test...")
            
            # Perform download test
            download_speed = self.st.download()
            
            # Convert from bits to megabits
            download_mbps = download_speed / 1_000_000
            
            self._update_progress(70, f"Download: {download_mbps:.2f} Mbps")
            self._update_status(f"📥 Download: {download_mbps:.2f} Mbps")
            
            return download_mbps
            
        except Exception as e:
            self._update_status(f"❌ Download test failed: {str(e)}")
            return 0.0
    
    def test_upload(self) -> float:
        """Test upload speed"""
        try:
            self._update_status("📤 Testing upload speed...")
            self._update_progress(80, "Starting upload test...")
            
            # Perform upload test
            upload_speed = self.st.upload()
            
            # Convert from bits to megabits
            upload_mbps = upload_speed / 1_000_000
            
            self._update_progress(90, f"Upload: {upload_mbps:.2f} Mbps")
            self._update_status(f"📤 Upload: {upload_mbps:.2f} Mbps")
            
            return upload_mbps
            
        except Exception as e:
            self._update_status(f"❌ Upload test failed: {str(e)}")
            return 0.0
    
    def get_ping(self) -> float:
        """Get ping/latency"""
        try:
            if self.st and self.st.best:
                ping = self.st.best['latency']
                self._update_status(f"🏓 Ping: {ping:.2f} ms")
                return ping
            return 0.0
            
        except Exception as e:
            self._update_status(f"❌ Ping test failed: {str(e)}")
            return 0.0
    
    def run_full_test(self) -> Dict:
        """Run complete speed test"""
        self.is_testing = True
        start_time = datetime.now()
        
        try:
            self._update_progress(0, "Initializing...")
            
            # Initialize
            if not self.initialize_test():
                self.is_testing = False
                return {}
            
            # Test download
            download_speed = self.test_download()
            
            # Test upload  
            upload_speed = self.test_upload()
            
            # Get ping
            ping = self.get_ping()
            
            # Compile results
            self.results = {
                'download_mbps': download_speed,
                'upload_mbps': upload_speed,
                'ping_ms': ping,
                'server_host': self.st.best['host'] if self.st and self.st.best else 'Unknown',
                'server_location': f"{self.st.best.get('name', 'Unknown')}, {self.st.best.get('country', 'Unknown')}" if self.st and self.st.best else 'Unknown',
                'isp': self.st.config.get('client', {}).get('isp', 'Unknown') if self.st else 'Unknown',
                'timestamp': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'test_duration': (datetime.now() - start_time).total_seconds()
            }
            
            self._update_progress(100, "Test completed!")
            self._update_status("✅ Speed test completed successfully!")
            
            self.is_testing = False
            return self.results
            
        except Exception as e:
            self._update_status(f"❌ Test failed: {str(e)}")
            self.is_testing = False
            return {}
    
    def run_test_threaded(self, completion_callback: Optional[Callable] = None):
        """Run speed test in a separate thread"""
        def test_thread():
            results = self.run_full_test()
            if completion_callback:
                completion_callback(results)
        
        thread = threading.Thread(target=test_thread, daemon=True)
        thread.start()
        return thread
    
    def get_server_info(self) -> Dict:
        """Get information about available servers"""
        try:
            if not self.st:
                self.st = speedtest.Speedtest()
                self.st.get_servers()
            
            servers = []
            for server_list in self.st.servers.values():
                for server in server_list[:5]:  # Limit to 5 servers per group
                    servers.append({
                        'id': server['id'],
                        'host': server['host'],
                        'name': server['name'],
                        'country': server['country'],
                        'distance': server['d']
                    })
            
            return {'servers': servers[:20]}  # Return top 20 servers
            
        except Exception as e:
            return {'error': str(e)}
    
    def test_specific_server(self, server_id: str) -> Dict:
        """Test with a specific server"""
        try:
            self.st = speedtest.Speedtest()
            self.st.get_servers([server_id])
            self.st.get_best_server()
            
            return self.run_full_test()
            
        except Exception as e:
            self._update_status(f"❌ Server test failed: {str(e)}")
            return {}
    
    def format_speed(self, speed_mbps: float) -> str:
        """Format speed for display"""
        if speed_mbps >= 1000:
            return f"{speed_mbps/1000:.2f} Gbps"
        else:
            return f"{speed_mbps:.2f} Mbps"
    
    def get_speed_rating(self, download_mbps: float) -> str:
        """Get speed rating based on download speed"""
        if download_mbps >= 100:
            return "🚀 Excellent"
        elif download_mbps >= 50:
            return "⚡ Very Good"
        elif download_mbps >= 25:
            return "👍 Good"
        elif download_mbps >= 10:
            return "👌 Fair"
        elif download_mbps >= 5:
            return "🐌 Slow"
        else:
            return "🚫 Very Slow"


def demo_speedtest():
    """Demonstrate speedtest functionality"""
    print("🌐 Internet Speed Test Demo")
    print("=" * 40)
    
    def progress_callback(progress, message):
        bar_length = 30
        filled_length = int(bar_length * progress // 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"\r[{bar}] {progress:.1f}% - {message}", end='', flush=True)
    
    def status_callback(status):
        print(f"\n{status}")
    
    # Create speedtest instance
    speed_test = SpeedTestCore()
    speed_test.set_callbacks(progress_callback, status_callback)
    
    # Run test
    results = speed_test.run_full_test()
    
    if results:
        print(f"\n\n📊 SPEED TEST RESULTS")
        print("-" * 30)
        print(f"📥 Download: {speed_test.format_speed(results['download_mbps'])}")
        print(f"📤 Upload: {speed_test.format_speed(results['upload_mbps'])}")
        print(f"🏓 Ping: {results['ping_ms']:.2f} ms")
        print(f"🎯 Server: {results['server_location']}")
        print(f"🌐 ISP: {results['isp']}")
        print(f"⭐ Rating: {speed_test.get_speed_rating(results['download_mbps'])}")
        print(f"⏱️ Test Duration: {results['test_duration']:.1f} seconds")
    else:
        print("❌ Speed test failed!")


if __name__ == "__main__":
    demo_speedtest()