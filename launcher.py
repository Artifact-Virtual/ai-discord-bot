#!/usr/bin/env python3
"""
Artifact Discord Bot Manager
Manages both Python bot and C++ Discord SDK components
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class DiscordBotManager:
    def __init__(self):
        self.bot_process = None
        self.sdk_process = None
        self.running = True
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.running = False
        self.cleanup()
        sys.exit(0)
        
    def check_requirements(self):
        """Check if all requirements are met"""
        print("🔍 Checking requirements...")
        
        # Check Python dependencies
        try:
            import discord
            import dotenv
            import requests
            print("✅ Python dependencies installed")
        except ImportError as e:
            print(f"❌ Missing Python dependency: {e}")
            print("Run: pip install -r requirements.txt")
            return False
            
        # Check .env file
        if not os.path.exists(".env"):
            print("❌ .env file not found")
            print("Please copy .env.example to .env and configure your Discord token")
            return False
        print("✅ .env file found")
        
        # Check C++ SDK build
        sdk_path = Path("build/Release/discord_sdk.exe")
        if not sdk_path.exists():
            print("⚠️  C++ Discord SDK not built")
            print("Run: build_sdk.bat to build the C++ components")
            return "python_only"
            
        print("✅ C++ Discord SDK available")
        return True
        
    def start_python_bot(self):
        """Start the Python Discord bot"""
        print("🐍 Starting Python Discord bot...")
        try:
            self.bot_process = subprocess.Popen(
                [sys.executable, "bot.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor bot output in a separate thread
            def monitor_bot():
                for line in iter(self.bot_process.stdout.readline, ''):
                    if line:
                        print(f"[Bot] {line.strip()}")
                        
            monitor_thread = threading.Thread(target=monitor_bot, daemon=True)
            monitor_thread.start()
            
            print("✅ Python bot started")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start Python bot: {e}")
            return False
            
    def start_cpp_sdk(self):
        """Start the C++ Discord SDK"""
        sdk_path = Path("build/Release/discord_sdk.exe")
        if not sdk_path.exists():
            print("⚠️  C++ SDK not available, skipping...")
            return False
            
        print("⚙️  Starting C++ Discord SDK...")
        try:
            self.sdk_process = subprocess.Popen(
                [str(sdk_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor SDK output in a separate thread
            def monitor_sdk():
                for line in iter(self.sdk_process.stdout.readline, ''):
                    if line:
                        print(f"[SDK] {line.strip()}")
                        
            monitor_thread = threading.Thread(target=monitor_sdk, daemon=True)
            monitor_thread.start()
            
            print("✅ C++ SDK started")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start C++ SDK: {e}")
            return False
            
    def cleanup(self):
        """Clean up all processes"""
        print("🧹 Cleaning up processes...")
        
        if self.bot_process:
            try:
                self.bot_process.terminate()
                self.bot_process.wait(timeout=5)
                print("✅ Python bot stopped")
            except subprocess.TimeoutExpired:
                self.bot_process.kill()
                print("🔄 Python bot force-stopped")
            except Exception as e:
                print(f"⚠️  Error stopping Python bot: {e}")
                
        if self.sdk_process:
            try:
                self.sdk_process.terminate()
                self.sdk_process.wait(timeout=5)
                print("✅ C++ SDK stopped")
            except subprocess.TimeoutExpired:
                self.sdk_process.kill()
                print("🔄 C++ SDK force-stopped")
            except Exception as e:
                print(f"⚠️  Error stopping C++ SDK: {e}")
                
    def run(self):
        """Main run loop"""
        print("🚀 Artifact Discord Bot Manager")
        print("=" * 40)
        
        # Check requirements
        req_status = self.check_requirements()
        if req_status is False:
            return 1
            
        # Start components
        success = False
        
        # Always try to start Python bot
        if self.start_python_bot():
            success = True
            
        # Start C++ SDK if available
        if req_status is True:  # Full requirements met
            self.start_cpp_sdk()
            
        if not success:
            print("❌ Failed to start any components")
            return 1
            
        print("\n🎉 Discord bot system is running!")
        print("📱 Python bot handles Discord commands and XP system")
        if req_status is True:
            print("🎮 C++ SDK provides rich presence and advanced features")
        print("🛑 Press Ctrl+C to stop all components")
        print("-" * 50)
        
        # Keep running until interrupted
        try:
            while self.running:
                # Check if processes are still alive
                if self.bot_process and self.bot_process.poll() is not None:
                    print("⚠️  Python bot process ended unexpectedly")
                    break
                    
                if self.sdk_process and self.sdk_process.poll() is not None:
                    print("⚠️  C++ SDK process ended unexpectedly")
                    # SDK ending is not critical, continue with just Python bot
                    self.sdk_process = None
                    
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Received Ctrl+C, shutting down...")
            
        finally:
            self.cleanup()
            
        print("👋 All components stopped. Goodbye!")
        return 0

def main():
    """Entry point"""
    os.chdir(Path(__file__).parent)  # Change to script directory
    manager = DiscordBotManager()
    return manager.run()

if __name__ == "__main__":
    sys.exit(main())
