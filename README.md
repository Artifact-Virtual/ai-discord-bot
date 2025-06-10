# 🤖 Artifact Discord Community Bot

A feature-rich Discord bot with AI integration, XP system, community management features, and C++ Discord SDK integration.

## 🚀 Features

- **AI Chat Integration**: Ask questions using Ollama AI models
- **XP/Level System**: Automatic XP tracking for active users
- **Rich Commands**: Modern Discord slash commands with embeds
- **C++ Discord SDK**: Rich presence and advanced Discord features
- **Error Handling**: Robust error handling and user feedback
- **Database**: SQLite database for persistent user data
- **Dual Architecture**: Python bot + C++ SDK working together

## 📋 Prerequisites

- Python 3.8+
- Discord Bot Token
- Ollama (optional, for AI features)

## 🛠️ Setup Instructions

### 1. Create Discord Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section
4. Create a bot and copy the token
5. Enable "Message Content Intent" in bot settings

### 2. Install Bot
```bash
# Install dependencies
pip install -r requirements.txt

# The .env file is already configured with your token
```

### 3. Invite Bot to Server
Use this URL (replace CLIENT_ID with your bot's client ID):
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot
```

### 4. Optional: Setup Ollama (for AI features)
```bash
# Install Ollama
# Visit: https://ollama.ai/download

# Pull a model (after installing Ollama)
ollama pull tinyllama:latest
```

## 🎮 Commands

| Command | Description |
|---------|-------------|
| `!ask <question>` | Ask the AI a question |
| `!stats [@user]` | Check XP and level stats |
| `!help` | Show all available commands |

## 🔧 Configuration

The bot is configured via the `.env` file:

```env
DISCORD_TOKEN=your_bot_token_here
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=tinyllama:latest
```

## 🚀 Running the Bot

### Option 1: Python Bot Only
```bash
python bot.py
```

### Option 2: Complete System (Python Bot + C++ SDK)
```bash
# First build the C++ SDK
build_sdk.bat

# Then run the complete system
python launcher.py
```

### Option 3: Legacy Simple Start
```bash
python start_bot.py
```

### Option 4: Windows Batch File
```batch
start_bot.bat
```

## ⚙️ C++ Discord SDK Integration

The bot now includes C++ Discord SDK integration for advanced features:

### Building the C++ SDK
```bash
# Build C++ components (requires Visual Studio 2022)
build_sdk.bat
```

### Features Provided by C++ SDK
- **Rich Presence**: Custom Discord activity status
- **Advanced Integration**: Native Discord features
- **Performance**: Low-level Discord API access
- **Enhanced User Experience**: Rich status displays

### Requirements for C++ SDK
- Visual Studio 2022 (or Visual Studio Build Tools)
- CMake 3.10+
- Discord Game SDK (included in lib/ directory)

## 📊 Database

The bot automatically creates an SQLite database (`artifact_bot.db`) with user stats:
- User ID
- XP Points
- Level (calculated from XP)

## 🔍 Troubleshooting

### Bot Won't Start
- Check your Discord token in `.env`
- Ensure Python 3.8+ is installed
- Run `pip install -r requirements.txt`

### AI Commands Not Working
- Make sure Ollama is running: `ollama serve`
- Check if the model is installed: `ollama list`
- Verify OLLAMA_URL in `.env`

### Permission Errors
- Ensure bot has necessary permissions in your Discord server
- Check that "Message Content Intent" is enabled

## 🔒 Security Notes

- Never share your Discord bot token
- The `.env` file should not be committed to version control
- Use appropriate Discord permissions (don't give Administrator unless needed)

## 📈 XP System

- Users gain 5 XP per message
- Level = XP ÷ 100 (minimum level 1)
- Stats persist in SQLite database

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 License

This project is part of the Artifact Virtual ecosystem.
