import sqlite3
import os

# This forces the file to be created in the same folder as this script
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aptistreak.db')

conn = sqlite3.connect(path)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER)")
c.execute("INSERT INTO test VALUES (1)") # This is the 'Seed'
conn.commit() # This is the command that creates the file
conn.close()

print(f"File created at: {path}")
