import sqlite3

# Connect to your SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the escorts table with WhatsApp and image fields
cursor.execute('''
    CREATE TABLE IF NOT EXISTS escorts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        whatsapp TEXT NOT NULL,
        image TEXT
    )
''')

# Insert dummy data (only if table is empty)
cursor.execute("SELECT COUNT(*) FROM escorts")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO escorts (name, whatsapp, image) VALUES (?, ?, ?)",
                   ('Precious', 'https://wa.me/2348123456789', 'images/style20.jpg'))

conn.commit()
conn.close()
