import sqlite3
import json

def init_db():
    """Initializes the SQLite database and creates tables if they don't exist."""
    conn = sqlite3.connect('aptistreak.db')
    c = conn.cursor()
    # Table for user stats and streak
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    streak INTEGER,
                    last_active TEXT,
                    total_solved INTEGER
                )''')
    # Table for performance history (stored as JSON for flexibility)
    c.execute('''CREATE TABLE IF NOT EXISTS performance (
                    user_id TEXT,
                    date TEXT,
                    score INTEGER,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )''')
    conn.commit()
    conn.close()

def load_user_data(user_id="default_user"):
    """Fetches user data from the database."""
    conn = sqlite3.connect('aptistreak.db')
    c = conn.cursor()
    c.execute("SELECT streak, last_active FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return {"streak": row[0], "last_active": row[1]}
    else:
        return {"streak": 0, "last_active": "Never"}

def save_user_action(user_id, streak, last_active):
    """Updates or inserts user streak data."""
    conn = sqlite3.connect('aptistreak.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO users (user_id, streak, last_active) 
                 VALUES (?, ?, ?)''', (user_id, streak, last_active))
    conn.commit()
    conn.close()

def log_score(user_id, date_str, score):
    """Logs a daily score into the performance table."""
    conn = sqlite3.connect('aptistreak.db')
    c = conn.cursor()
    c.execute("INSERT INTO performance (user_id, date, score) VALUES (?, ?, ?)", 
              (user_id, date_str, score))
    conn.commit()
    conn.close()

def get_history(user_id="default_user"):
    """Retrieves all historical scores for plotting."""
    conn = sqlite3.connect('aptistreak.db')
    c = conn.cursor()
    c.execute("SELECT date, score FROM performance WHERE user_id=? ORDER BY date ASC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [{"date": r[0], "score": r[1]} for r in rows]
