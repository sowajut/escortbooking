from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row # To get dictionary-like rows
    return conn

# Create table if it doesn't exist
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            booking_time TEXT NOT NULL,
            duration TEXT NOT NULL,
            location_type TEXT NOT NULL,
            escort TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS escorts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    # Sample escort
    cursor.execute("INSERT OR IGNORE INTO escorts (id, name) VALUES (1, 'Precious')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/escorts', methods=['GET', 'POST'])
def escort_list():
    conn = get_db_connection()

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        booking_date = request.form['booking_date']
        hour = request.form['hour']
        minute = request.form['minute']
        ampm = request.form['ampm']
        duration = request.form['duration']
        location_type = request.form['location_type']
        escort_name = request.form['escort']

        # Format time
        booking_time = f"{hour}:{minute} {ampm}"

        # Save booking to database
        conn.execute('''
            INSERT INTO bookings (
                full_name, email, phone, booking_date,
                booking_time, duration, location_type, escort
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (full_name, email, phone, booking_date,
              booking_time, duration, location_type, escort_name))
        conn.commit()
        conn.close()

        # Format WhatsApp message
        message = f"Hi Precious, I just booked a session.\n\n" \
                  f"Name: {full_name}\n" \
                  f"Phone: {phone}\n" \
                  f"Date: {booking_date}\n" \
                  f"Time: {booking_time}\n" \
                  f"Duration: {duration}\n" \
                  f"Location: {location_type}"

        encoded_message = message.replace(" ", "%20").replace("\n", "%0A")

        # Replace with Precious's actual WhatsApp number (with country code, no +)
        precious_number = "2348123456789"
        wa_link = f"https://wa.me/{precious_number}?text={encoded_message}"
        return redirect(wa_link)

    # If GET request
    escorts = conn.execute('SELECT * FROM escorts').fetchall()
    conn.close()
    return render_template('escort-list.html', escorts=escorts)
    
if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
