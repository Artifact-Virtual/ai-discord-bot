# Artifact Discord Bot Management Script for Windows
# PowerShell script to manage the Discord bot system

param(
    [Parameter(Position=0)]
    [ValidateSet("start", "stop", "status", "build", "install", "help")]
    [string]$Action = "help"
)

# Colors for output
$Colors = @{
    Success = "Green"
    Warning = "Yellow" 
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
}

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Show-Header {
    Write-ColorOutput "🤖 Artifact Discord Bot Manager" "Header"
    Write-ColorOutput "=================================" "Header"
    Write-ColorOutput "Current Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" "Info"
    Write-ColorOutput ""
}

function Show-Help {
    Write-ColorOutput "Available Commands:" "Info"
    Write-ColorOutput "  start    - Start the Discord bot system" "Success"
    Write-ColorOutput "  stop     - Stop all Discord bot processes" "Warning"
    Write-ColorOutput "  status   - Show system status" "Info"
    Write-ColorOutput "  build    - Build C++ Discord SDK" "Info"
    Write-ColorOutput "  install  - Install Python dependencies" "Info"
    Write-ColorOutput "  help     - Show this help message" "Info"
    Write-ColorOutput ""
    Write-ColorOutput "Examples:" "Info"
    Write-ColorOutput "  .\manage.ps1 start" "Success"
    Write-ColorOutput "  .\manage.ps1 status" "Info"
    Write-ColorOutput "  .\manage.ps1 build" "Info"
}

function Test-Prerequisites {
    Write-ColorOutput "🔍 Checking prerequisites..." "Info"
    
    # Check Python
    try {
        $pythonVersion = python --version 2>$null
        if ($pythonVersion) {
            Write-ColorOutput "✅ Python found: $pythonVersion" "Success"
        } else {
            Write-ColorOutput "❌ Python not found in PATH" "Error"
            return $false
        }
    } catch {
        Write-ColorOutput "❌ Python not found" "Error"
        return $false
    }
    
    # Check .env file
    if (Test-Path ".env") {
        Write-ColorOutput "✅ .env file found" "Success"
    } else {
        Write-ColorOutput "❌ .env file not found" "Error"
        Write-ColorOutput "💡 Copy .env.example to .env and configure your Discord token" "Warning"
        return $false
    }
    
    return $true
}

function Install-Dependencies {
    Write-ColorOutput "📦 Installing Python dependencies..." "Info"
    
    try {
        $result = python -m pip install -r requirements.txt 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Dependencies installed successfully" "Success"
            return $true
        } else {
            Write-ColorOutput "❌ Failed to install dependencies" "Error"
            Write-ColorOutput $result "Error"
            return $false
        }
    } catch {
        Write-ColorOutput "❌ Error installing dependencies: $_" "Error"
        return $false
    }
}

function Build-CppSdk {
    Write-ColorOutput "🔨 Building C++ Discord SDK..." "Info"
    
    if (Test-Path "build_sdk.bat") {
        try {
            & .\build_sdk.bat
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput "✅ C++ SDK built successfully" "Success"
                return $true
            } else {
                Write-ColorOutput "❌ C++ SDK build failed" "Error"
                return $false
            }
        } catch {
            Write-ColorOutput "❌ Error building C++ SDK: $_" "Error"
            return $false
        }
    } else {
        Write-ColorOutput "❌ build_sdk.bat not found" "Error"
        return $false
    }
}

function Start-DiscordBot {
    Write-ColorOutput "🚀 Starting Discord bot system..." "Info"
    
    if (-not (Test-Prerequisites)) {
        Write-ColorOutput "❌ Prerequisites not met" "Error"
        return
    }
    
    # Check if launcher.py exists for complete system
    if (Test-Path "launcher.py") {
        Write-ColorOutput "🎯 Starting complete system (Python + C++ SDK)..." "Info"
        try {
            Start-Process python -ArgumentList "launcher.py" -NoNewWindow -PassThru
            Write-ColorOutput "✅ Complete system started" "Success"
            Write-ColorOutput "💡 Monitor the console for status updates" "Info"
        } catch {
            Write-ColorOutput "❌ Failed to start complete system: $_" "Error"
        }
    } else {
        Write-ColorOutput "🐍 Starting Python bot only..." "Info"
        try {
            Start-Process python -ArgumentList "bot.py" -NoNewWindow -PassThru
            Write-ColorOutput "✅ Python bot started" "Success"
        } catch {
            Write-ColorOutput "❌ Failed to start Python bot: $_" "Error"
        }
    }
}

function Stop-DiscordBot {
    Write-ColorOutput "🛑 Stopping Discord bot processes..." "Warning"
    
    try {
        # Stop Python processes running bot.py
        $pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*bot.py*" -or $_.CommandLine -like "*launcher.py*"}
        if ($pythonProcesses) {
            $pythonProcesses | Stop-Process -Force
            Write-ColorOutput "✅ Python bot processes stopped" "Success"
        } else {
            Write-ColorOutput "ℹ️  No Python bot processes found" "Info"
        }
        
        # Stop C++ SDK processes
        $cppProcesses = Get-Process discord_sdk -ErrorAction SilentlyContinue
        if ($cppProcesses) {
            $cppProcesses | Stop-Process -Force
            Write-ColorOutput "✅ C++ SDK processes stopped" "Success"
        } else {
            Write-ColorOutput "ℹ️  No C++ SDK processes found" "Info"
        }
        
    } catch {
        Write-ColorOutput "❌ Error stopping processes: $_" "Error"
    }
}

function Show-Status {
    Write-ColorOutput "📊 Running system status check..." "Info"
    
    if (Test-Path "status.py") {
        try {
            python status.py
        } catch {
            Write-ColorOutput "❌ Error running status check: $_" "Error"
        }
    } else {
        Write-ColorOutput "❌ status.py not found" "Error"
        Write-ColorOutput "💡 Basic status check:" "Info"
        
        # Basic checks
        if (Test-Path ".env") {
            Write-ColorOutput "✅ .env file exists" "Success"
        } else {
            Write-ColorOutput "❌ .env file missing" "Error"
        }
        
        if (Test-Path "bot.py") {
            Write-ColorOutput "✅ bot.py exists" "Success"
        } else {
            Write-ColorOutput "❌ bot.py missing" "Error"
        }
    }
}

# Main script execution
Clear-Host
Show-Header

# Change to script directory
Set-Location $PSScriptRoot

switch ($Action.ToLower()) {
    "start" {
        Start-DiscordBot
    }
    "stop" {
        Stop-DiscordBot
    }
    "status" {
        Show-Status
    }
    "build" {
        Build-CppSdk
    }
    "install" {
        Install-Dependencies
    }
    "help" {
        Show-Help
    }
    default {
        Write-ColorOutput "❌ Unknown action: $Action" "Error"
        Show-Help
    }
}

Write-ColorOutput ""
Write-ColorOutput "💡 Use '.\manage.ps1 help' for more information" "Info"
