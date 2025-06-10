#!/usr/bin/env python3
"""
Discord Bot System Status Checker
Provides comprehensive status information for the Artifact Discord Bot system
"""

import os
import sys
import subprocess
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import requests

def print_header():
    """Print status header"""
    print("🤖 Artifact Discord Bot System Status")
    print("=" * 50)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💻 OS: {os.name}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print("-" * 50)

def check_environment():
    """Check environment configuration"""
    print("🔍 Environment Configuration:")
    
    # Check .env file
    env_path = Path(".env")
    if env_path.exists():
        print("  ✅ .env file found")
        
        with open(env_path) as f:
            content = f.read()
            
        # Check Discord token
        if "DISCORD_TOKEN=" in content and "your-discord-bot-token-here" not in content:
            print("  ✅ Discord token configured")
        else:
            print("  ❌ Discord token not configured")
            
        # Check Ollama configuration
        if "OLLAMA_URL=" in content:
            print("  ✅ Ollama URL configured")
        else:
            print("  ⚠️  Ollama URL not configured")
            
    else:
        print("  ❌ .env file not found")
        
    print()

def check_dependencies():
    """Check Python dependencies"""
    print("📦 Python Dependencies:")
    
    required_packages = [
        "discord.py",
        "python-dotenv", 
        "requests",
        "aiohttp"
    ]
    
    for package in required_packages:
        try:
            if package == "discord.py":
                import discord
                print(f"  ✅ {package} v{discord.__version__}")
            elif package == "python-dotenv":
                import dotenv
                print(f"  ✅ {package}")
            elif package == "requests":
                import requests
                print(f"  ✅ {package} v{requests.__version__}")
            elif package == "aiohttp":
                import aiohttp
                print(f"  ✅ {package} v{aiohttp.__version__}")
        except ImportError:
            print(f"  ❌ {package} not installed")
            
    print()

def check_database():
    """Check database status"""
    print("🗄️  Database Status:")
    
    db_path = Path("artifact_bot.db")
    if db_path.exists():
        print(f"  ✅ Database file exists ({db_path.stat().st_size} bytes)")
        
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Check users table
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"  📊 Total users: {user_count}")
            
            # Check total XP
            cursor.execute("SELECT SUM(xp) FROM users")
            total_xp = cursor.fetchone()[0] or 0
            print(f"  🏆 Total XP distributed: {total_xp}")
            
            # Check highest level user
            cursor.execute("SELECT MAX(level) FROM users")
            max_level = cursor.fetchone()[0] or 0
            print(f"  🥇 Highest user level: {max_level}")
            
            conn.close()
            
        except Exception as e:
            print(f"  ❌ Database error: {str(e)}")
    else:
        print("  ⚠️  Database file not found (will be created on first run)")
        
    print()

def check_cpp_sdk():
    """Check C++ SDK build status"""
    print("⚙️  C++ Discord SDK:")
    
    # Check if CMakeLists.txt exists
    cmake_path = Path("CMakeLists.txt")
    if cmake_path.exists():
        print("  ✅ CMakeLists.txt found")
    else:
        print("  ❌ CMakeLists.txt not found")
        
    # Check build directory
    build_path = Path("build")
    if build_path.exists():
        print("  ✅ Build directory exists")
        
        # Check for executable
        exe_path = build_path / "Release" / "discord_sdk.exe"
        if exe_path.exists():
            print(f"  ✅ Discord SDK executable built ({exe_path.stat().st_size} bytes)")
            print(f"     📍 Location: {exe_path.absolute()}")
        else:
            print("  ⚠️  Discord SDK executable not found")
            print("     💡 Run 'build_sdk.bat' to build the C++ SDK")
    else:
        print("  ⚠️  Build directory not found")
        print("     💡 Run 'build_sdk.bat' to build the C++ SDK")
        
    # Check for Discord SDK library
    lib_path = Path("lib/discord_social_sdk")
    if lib_path.exists():
        print("  ✅ Discord SDK library directory found")
    else:
        print("  ❌ Discord SDK library directory not found")
        
    print()

def check_ollama_connection():
    """Check Ollama service status"""
    print("🦙 Ollama Service:")
    
    try:
        # Try to connect to Ollama
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"  ✅ Ollama service running")
            print(f"  📋 Available models: {len(models)}")
            for model in models[:3]:  # Show first 3 models
                print(f"     • {model.get('name', 'Unknown')}")
            if len(models) > 3:
                print(f"     ... and {len(models) - 3} more")
        else:
            print(f"  ⚠️  Ollama service responded with status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("  ❌ Cannot connect to Ollama service")
        print("     💡 Make sure Ollama is installed and running")
        print("     💡 Visit: https://ollama.ai/download")
    except requests.exceptions.Timeout:
        print("  ⚠️  Ollama service timeout")
    except Exception as e:
        print(f"  ❌ Ollama check error: {str(e)}")
        
    print()

def check_running_processes():
    """Check for running Discord bot processes"""
    print("🔄 Running Processes:")
    
    try:
        # Check for Python processes running bot.py
        result = subprocess.run([
            "powershell", "-Command", 
            "Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like '*bot.py*'}"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            print("  ✅ Discord bot Python process is running")
        else:
            print("  ⚠️  No Discord bot Python process found")
            
        # Check for C++ SDK process
        result = subprocess.run([
            "powershell", "-Command",
            "Get-Process discord_sdk -ErrorAction SilentlyContinue"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            print("  ✅ Discord C++ SDK process is running")
        else:
            print("  ⚠️  No Discord C++ SDK process found")
            
    except Exception as e:
        print(f"  ❌ Process check error: {str(e)}")
        
    print()

def check_network_connectivity():
    """Check network connectivity to Discord"""
    print("🌐 Network Connectivity:")
    
    try:
        # Test Discord API connectivity
        response = requests.get("https://discord.com/api/v10/gateway", timeout=10)
        if response.status_code == 200:
            print("  ✅ Discord API reachable")
        else:
            print(f"  ⚠️  Discord API returned status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("  ❌ Cannot reach Discord API")
        print("     💡 Check internet connection")
    except requests.exceptions.Timeout:
        print("  ⚠️  Discord API timeout")
    except Exception as e:
        print(f"  ❌ Network check error: {str(e)}")
        
    print()

def print_recommendations():
    """Print system recommendations"""
    print("💡 Recommendations:")
    print("  • Use 'python launcher.py' to start both Python bot and C++ SDK")
    print("  • Use 'python bot.py' to start only the Python bot")
    print("  • Run 'build_sdk.bat' to build the C++ Discord SDK components")
    print("  • Use VS Code tasks (Ctrl+Shift+P > Tasks: Run Task) for easy management")
    print("  • Monitor logs for any error messages during operation")
    print()

def main():
    """Main status check function"""
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    print_header()
    check_environment()
    check_dependencies()
    check_database()
    check_cpp_sdk()
    check_ollama_connection()
    check_running_processes()
    check_network_connectivity()
    print_recommendations()
    
    print("✅ Status check complete!")

if __name__ == "__main__":
    main()
