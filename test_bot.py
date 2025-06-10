"""
Discord Bot Test Suite
Comprehensive testing of all bot functionality
"""
import asyncio
import os
import sqlite3
from datetime import datetime

import discord
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()

class BotTester:
    def __init__(self):
        self.token = os.getenv('DISCORD_TOKEN')
        self.guild_id = None
        self.channel_id = None
        
    async def test_connection(self):
        """Test basic Discord connection"""
        print("🔗 Testing Discord Connection...")
        
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            print(f"✅ Connected as {client.user}")
            print(f"📊 Connected to {len(client.guilds)} guilds")
            
            if client.guilds:
                guild = client.guilds[0]
                self.guild_id = guild.id
                print(f"🏠 Primary guild: {guild.name} (ID: {guild.id})")
                
                # Find a text channel
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        self.channel_id = channel.id
                        print(f"💬 Test channel: {channel.name} (ID: {channel.id})")
                        break
            
            await client.close()
        
        try:
            await client.start(self.token)
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
        
        return True
    
    def test_database(self):
        """Test database functionality"""
        print("\n🗄️ Testing Database...")
        
        try:
            conn = sqlite3.connect('artifact_bot.db')
            cursor = conn.cursor()
            
            # Check if tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📋 Database tables: {[table[0] for table in tables]}")
            
            # Check user stats
            cursor.execute("SELECT COUNT(*) FROM user_stats")
            user_count = cursor.fetchone()[0]
            print(f"👥 Total users: {user_count}")
            
            cursor.execute("SELECT SUM(xp) FROM user_stats")
            total_xp = cursor.fetchone()[0] or 0
            print(f"🏆 Total XP: {total_xp}")
            
            conn.close()
            print("✅ Database test successful")
            return True
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            return False
    
    def test_ollama(self):
        """Test Ollama integration"""
        print("\n🦙 Testing Ollama Integration...")
        
        try:
            ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
            
            # Test connection
            response = requests.get(f"{ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                print(f"✅ Ollama connected, {len(models)} models available")
                
                # Test a simple query
                test_payload = {
                    "model": "tinyllama",
                    "prompt": "Say hello",
                    "stream": False
                }
                
                response = requests.post(f"{ollama_url}/api/generate", json=test_payload, timeout=10)
                if response.status_code == 200:
                    print("✅ Ollama test query successful")
                    return True
                else:
                    print(f"⚠️ Ollama query failed: {response.status_code}")
                    return False
            else:
                print(f"❌ Ollama not accessible: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Ollama test failed: {e}")
            return False
    
    def test_configuration(self):
        """Test configuration files"""
        print("\n⚙️ Testing Configuration...")
        
        tests = []
        
        # Check .env file
        if os.path.exists('.env'):
            print("✅ .env file found")
            tests.append(True)
        else:
            print("❌ .env file missing")
            tests.append(False)
        
        # Check Discord token
        if self.token:
            print("✅ Discord token configured")
            tests.append(True)
        else:
            print("❌ Discord token missing")
            tests.append(False)
        
        # Check requirements.txt
        if os.path.exists('requirements.txt'):
            print("✅ requirements.txt found")
            tests.append(True)
        else:
            print("❌ requirements.txt missing")
            tests.append(False)
        
        # Check bot files
        bot_files = ['bot.py', 'db.py', 'ollama_client.py']
        for file in bot_files:
            if os.path.exists(file):
                print(f"✅ {file} found")
                tests.append(True)
            else:
                print(f"❌ {file} missing")
                tests.append(False)
        
        return all(tests)
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🧪 Discord Bot Test Suite")
        print("=" * 50)
        print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        results = []
        
        # Configuration test
        results.append(self.test_configuration())
        
        # Database test
        results.append(self.test_database())
        
        # Ollama test
        results.append(self.test_ollama())
        
        # Discord connection test
        results.append(await self.test_connection())
        
        print("\n" + "=" * 50)
        print("📊 Test Results Summary:")
        print(f"✅ Passed: {sum(results)}")
        print(f"❌ Failed: {len(results) - sum(results)}")
        print(f"📈 Success Rate: {(sum(results)/len(results)*100):.1f}%")
        
        if all(results):
            print("\n🎉 All tests passed! Bot is ready for use.")
            print("\n💡 Next steps:")
            print("   • Use 'python bot.py' to start the bot")
            print("   • Use 'python launcher.py' for full system")
            print("   • Test commands in Discord: !help, !ask, !stats")
        else:
            print("\n⚠️ Some tests failed. Check the issues above.")
        
        return all(results)

async def main():
    tester = BotTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
