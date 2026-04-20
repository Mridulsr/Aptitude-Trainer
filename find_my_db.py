import sqlite3
import os

# 1. Force the path to this exact folder
current_folder = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_folder, 'aptistreak.db')

try:
    # 2. Create the file and a table
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS location_test (id INTEGER)")
    c.execute("INSERT INTO location_test VALUES (100)")
    conn.commit()
    conn.close()
    
    print("-" * 50)
    print("✅ FILE CREATED SUCCESSFULLY!")
    print(f"📍 EXACT LOCATION: {db_path}")
    print("-" * 50)
    print("Copy the location above and paste it into DB Browser's 'Open Database' window.")

except Exception as e:
    print(f"❌ Error: {e}")
