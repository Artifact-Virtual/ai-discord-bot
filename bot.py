import discord
from discord.ext import commands
from db import init_db, add_xp, get_user_stats
from ollama_client import ask_ollama
import os
from dotenv import load_dotenv
import subprocess
import time
import socket
import requests
import logging

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN or TOKEN == "your-discord-bot-token-here":
    print("❌ Error: Please set your DISCORD_TOKEN in the .env file")
    print("1. Go to https://discord.com/developers/applications")
    print("2. Create a new application and bot")
    print("3. Copy the bot token to your .env file")
    exit(1)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# --- Enterprise logging setup ---
logging.basicConfig(
    filename='discord_bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def is_ollama_running(host='localhost', port=11434):
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except Exception:
        return False

def ensure_ollama_and_model(model_name='tinyllama:latest', max_wait=30):
    # Start Ollama server if not running
    if not is_ollama_running():
        print("🔄 Ollama server not detected. Starting Ollama...")
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Wait for Ollama to start
        for _ in range(max_wait):
            if is_ollama_running():
                print("✅ Ollama server is running.")
                break
            time.sleep(1)
        else:
            raise RuntimeError("❌ Ollama server failed to start.")
    else:
        print("✅ Ollama server is already running.")

    # Check if model is available
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        if resp.status_code == 200 and model_name.split(":")[0] in resp.text:
            print(f"✅ {model_name} model is already pulled.")
            return
    except Exception:
        pass
    print(f"🔄 Pulling {model_name} model...")
    subprocess.run(["ollama", "pull", model_name], check=False)
    print(f"✅ {model_name} model is ready.")

def ollama_health_check():
    """Check if Ollama server and model are available."""
    import requests
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        if resp.status_code == 200 and 'tinyllama' in resp.text:
            return True
    except Exception as e:
        logging.error(f"Ollama health check failed: {e}")
    return False

# --- Enterprise-level improvements ---
# 1. Ensure Ollama and model before bot starts
# 2. Add robust error handling and logging
# 3. Add health check endpoint (optional for ops)
# 4. Add graceful shutdown for subprocesses (future)
# 5. Add startup diagnostics

try:
    ensure_ollama_and_model()
except Exception as e:
    print(f"[Startup Error] {e}")
    exit(1)

@bot.event
async def on_ready():
    print(f"[BOT] {bot.user} is now online!")
    print(f"[STATS] Connected to {len(bot.guilds)} guilds")
    init_db()
    # Set bot status
    activity = discord.Activity(type=discord.ActivityType.listening, name="!help for commands")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Add XP for active users
    add_xp(str(message.author.id), 5)
    
    # Process bot commands
    await bot.process_commands(message)

@bot.command(name='ask')
async def ask_command(ctx, *, question):
    """Ask the AI a question using !ask <your question>"""
    if not question:
        await ctx.send("[?] Please provide a question! Usage: `!ask <your question>`")
        return
    if not ollama_health_check():
        await ctx.send("[X] Ollama AI backend is not available. Please try again later or contact support.")
        logging.error("Ollama backend unavailable when answering user question.")
        return
    async with ctx.typing():
        try:
            reply = ask_ollama(question)
            # Split long messages if needed
            if len(reply) > 2000:
                chunks = [reply[i:i+2000] for i in range(0, len(reply), 2000)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(reply)
        except Exception as e:
            await ctx.send(f"[X] Error processing your request: {str(e)}")
            logging.error(f"Error in ask_command: {e}")

@bot.command(name='stats')
async def stats_command(ctx, member: discord.Member = None):
    """Check your or someone else's XP and level"""
    target = member or ctx.author
    user_id = str(target.id)
    try:
        stats = get_user_stats(user_id)
        if stats:
            xp, level = stats
            embed = discord.Embed(
                title=f"[STATS] Stats for {target.display_name}",
                color=0x00ff00
            )
            embed.add_field(name="Level", value=level, inline=True)
            embed.add_field(name="XP", value=xp, inline=True)
            embed.set_thumbnail(url=target.avatar.url if target.avatar else None)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"[i] No stats found for {target.display_name}")
    except Exception as e:
        await ctx.send(f"[X] Error retrieving stats: {str(e)}")

@bot.command(name='help')
async def help_command(ctx):
    """Show available commands"""
    embed = discord.Embed(
        title="[BOT] Artifact Discord Bot Commands",
        description="Here are the available commands:",
        color=0x0099ff
    )
    embed.add_field(
        name="!ask <question>", 
        value="Ask the AI a question", 
        inline=False
    )
    embed.add_field(
        name="!stats [@user]", 
        value="Check XP and level stats", 
        inline=False
    )
    embed.add_field(
        name="!help", 
        value="Show this help message", 
        inline=False
    )
    embed.set_footer(text="Powered by Artifact Virtual System")
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("[?] Unknown command! Use `!help` to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"[X] Missing required argument: {error.param}")
    else:
        await ctx.send(f"[X] An error occurred: {str(error)}")
        print(f"Error in command {ctx.command}: {error}")

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid Discord token! Please check your .env file.")
    except Exception as e:
        print(f"❌ Failed to start bot: {str(e)}")
