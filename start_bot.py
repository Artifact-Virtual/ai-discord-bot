#!/usr/bin/env python3
"""
Discord Community Bot Startup Script
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_env_file():
    """Check if .env file exists and has token"""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found")
        print("Please copy .env.example to .env and add your Discord bot token")
        return False
    
    with open(env_path) as f:
        content = f.read()
        if "your-discord-bot-token-here" in content:
            print("❌ Please set your Discord bot token in .env file")
            print("Visit: https://discord.com/developers/applications")
            return False
    
    print("✅ .env file configured")
    return True

def main():
    """Main startup function"""
    print("🤖 Artifact Discord Bot Startup")
    print("=" * 40)
    
    if not check_python_version():
        return 1
    
    if not install_dependencies():
        return 1
    
    if not check_env_file():
        return 1
    
    print("\n🚀 Starting Discord bot...")
    try:
        subprocess.run([sys.executable, "bot.py"])
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot crashed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
