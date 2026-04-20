import sqlite3
import os

# Get the exact folder where this script is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'aptistreak.db')

def force_init():
    print(f"Creating database at: {db_path}")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 1. Create Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (user_id TEXT PRIMARY KEY, streak INTEGER, last_active TEXT)''')
    
    # 2. Create Performance Table
    c.execute('''CREATE TABLE IF NOT EXISTS performance 
                 (user_id TEXT, date TEXT, score INTEGER)''')
    
    # 3. Insert a dummy "Seed" value to force the file to save to disk
    c.execute("INSERT OR IGNORE INTO users VALUES ('guest_pro', 0, 'Never')")
    
    conn.commit()
    conn.close()
    print("✅ Success! 'aptistreak.db' has been created.")

if __name__ == "__main__":
    force_init()
