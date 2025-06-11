# Artifact Discord Community Bot

A feature-rich Discord bot with AI integration, XP system, community management tools, and C++ Discord SDK support.

## Features

- **AI Chat Integration:** Ask questions using Ollama AI models
- **XP/Level System:** Automatically tracks XP for active users
- **Modern Slash Commands:** Rich, user-friendly command interface
- **C++ Discord SDK Integration:** Adds rich presence and advanced features
- **Robust Error Handling:** User feedback and stability features
- **SQLite Database:** Persistent storage for user data
- **Dual Architecture:** Python bot core with C++ SDK extension

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- Ollama (optional, for AI functionality)

## Setup Instructions

1.  **Create a Discord Bot**
    1.  Visit the [Discord Developer Portal](https://discord.com/developers/applications)
    2.  Create a new application
    3.  Navigate to the "Bot" section
    4.  Add a bot and copy its token
    5.  Enable the "Message Content Intent" under Privileged Gateway Intents

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

    > The `.env` file should be configured with your bot token and other settings.

3.  **Invite the Bot to Your Server**

    Replace `YOUR_CLIENT_ID` with your bot's actual Client ID:

    ```
    https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot
    ```

4.  **Optional: Set Up Ollama for AI Features**

    ```bash
    # Install Ollama (see: https://ollama.ai/download)
    # Pull the model
    ollama pull tinyllama:latest
    ```

## Available Commands

| Command          | Description                      |
| ---------------- | -------------------------------- |
| `!ask <question>` | Ask the AI a question            |
| `!stats [@user]`  | View XP and level information    |
| `!help`           | List all available commands      |

## Configuration

Set your environment variables in the `.env` file:

```
DISCORD_TOKEN=your_bot_token_here
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=tinyllama:latest
```

## Running the Bot

**Option 1: Run Python Bot Only**

```bash
python bot.py
```

**Option 2: Full System (Python Bot + C++ SDK)**

```bash
# Build C++ SDK components
build_sdk.bat

# Run the combined system
python launcher.py
```

**Option 3: Simple Legacy Startup**

```bash
python start_bot.py
```

**Option 4: Windows Batch Startup**

```bash
start_bot.bat
```

## C++ Discord SDK Integration

### Building the SDK

```bash
# Requires Visual Studio 2022
build_sdk.bat
```

### Features Enabled

- Custom rich presence on Discord
- Access to native Discord SDK features
- Improved performance and native-level functionality

### Requirements

- Visual Studio 2022 or Build Tools
- CMake 3.10 or higher
- Discord Game SDK (provided in `lib/` directory)

## Database

The bot uses an SQLite database (`artifact_bot.db`) to store user stats:

- Discord User ID
- XP points
- Calculated level based on XP

## Troubleshooting

### Bot Fails to Start

- Confirm your Discord token is correct in `.env`
- Ensure Python 3.8+ is installed
- Reinstall dependencies: `pip install -r requirements.txt`

### AI Commands Not Responding

- Make sure Ollama is running: `ollama serve`
- Ensure your model is installed: `ollama list`
- Confirm `OLLAMA_URL` is correct in `.env`

### Permissions Issues

- Confirm bot has necessary permissions in your Discord server
- Ensure "Message Content Intent" is enabled in the Developer Portal

## Security Guidelines

- Never share your Discord bot token
- Do not commit the `.env` file to public repositories
- Use the minimum required permissions for your bot

## XP and Level System

- Users gain 5 XP per message
- Level is calculated as XP ÷ 100, with a minimum level of 1
- All stats are stored persistently in SQLite

## Contributing

1.  Fork the repository
2.  Create a new feature branch
3.  Implement your changes
4.  Test thoroughly
5.  Submit a pull request

## License

This project is part of the Artifact Virtual ecosystem. Please refer to the `LICENSE` file for more information.
