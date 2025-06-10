@echo off
echo 🔨 Simple Discord SDK Build (No CMake Required)
echo ================================================
echo.

:: Check for Visual Studio Build Tools
where cl >nul 2>&1
if errorlevel 1 (
    echo ❌ Visual Studio Build Tools not found
    echo 💡 Install Visual Studio 2019/2022 Build Tools or use Visual Studio Developer Command Prompt
    echo    Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    pause
    exit /b 1
)

:: Create build directory
if not exist "build" mkdir build
cd build

echo ✅ Found Visual Studio Build Tools
echo 🔧 Compiling Discord SDK...

:: Simple compilation without CMake
cl /EHsc /std:c++17 /I"..\discord_social_sdk\include" /I".." ^
   "..\discord_sdk.cpp" ^
   "..\discord_social_sdk\lib\release\discord_partner_sdk.lib" ^
   /Fe:discord_sdk.exe

if errorlevel 1 (
    echo ❌ Compilation failed
    pause
    exit /b 1
)

echo ✅ Build completed successfully!
echo 📁 Executable: build\discord_sdk.exe
echo.
echo 💡 To run: .\build\discord_sdk.exe
echo 💡 Or use: python launcher.py
pause
