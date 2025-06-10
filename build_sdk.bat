@echo off
echo 🔨 Building Artifact Discord SDK...
echo =====================================

REM Check if CMake is installed
cmake --version >nul 2>&1
if errorlevel 1 (
    echo ❌ CMake is not installed or not in PATH
    echo Please install CMake from https://cmake.org/download/
    pause
    exit /b 1
)

REM Create build directory
if not exist "build" mkdir build
cd build

REM Configure the project
echo 📋 Configuring CMake project...
cmake .. -G "Visual Studio 17 2022" -A x64

if errorlevel 1 (
    echo ❌ CMake configuration failed
    pause
    exit /b 1
)

REM Build the project
echo 🔨 Building project...
cmake --build . --config Release

if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo ✅ Build completed successfully!
echo 📁 Executables are in: build/Release/
echo 🚀 To run Discord SDK: build/Release/discord_sdk.exe
echo 🤖 To run Python bot: python bot.py

pause
