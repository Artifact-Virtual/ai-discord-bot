@echo off
echo 🤖 Starting Artifact Discord Bot...
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found
    echo Please copy .env.example to .env and configure your Discord token
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Start the bot
echo 🚀 Starting Discord bot...
python bot.py

pause
