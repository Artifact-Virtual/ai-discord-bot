
import sqlite3

def init_db():
    """Initialize the database with user stats table"""
    try:
        conn = sqlite3.connect('artifact_bot.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY,
                        xp INTEGER DEFAULT 0,
                        level INTEGER DEFAULT 1
                    )''')
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {str(e)}")

def add_xp(user_id, amount):
    """Add XP to a user and calculate their level"""
    try:
        conn = sqlite3.connect('artifact_bot.db')
        c = conn.cursor()
        
        # Insert user if they don't exist
        c.execute('INSERT OR IGNORE INTO users (id) VALUES (?)', (user_id,))
        
        # Add XP
        c.execute('UPDATE users SET xp = xp + ? WHERE id = ?', (amount, user_id))
        
        # Calculate and update level (100 XP per level)
        c.execute('SELECT xp FROM users WHERE id = ?', (user_id,))
        xp = c.fetchone()[0]
        new_level = max(1, xp // 100)
        c.execute('UPDATE users SET level = ? WHERE id = ?', (new_level, user_id))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Error adding XP: {str(e)}")

def get_user_stats(user_id):
    """Get user's XP and level"""
    try:
        conn = sqlite3.connect('artifact_bot.db')
        c = conn.cursor()
        c.execute('SELECT xp, level FROM users WHERE id = ?', (user_id,))
        result = c.fetchone()
        conn.close()
        return result if result else (0, 1)
    except Exception as e:
        print(f"❌ Error getting user stats: {str(e)}")
        return (0, 1)
