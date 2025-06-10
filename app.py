from flask import Flask, request, jsonify
from datetime import datetime
import pytz
import sqlite3
import os

app = Flask(__name__)

# Connect to SQLite DB
DB_NAME = "fitness.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    instructor TEXT,
    datetime TEXT,
    slots INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id TEXT,
    client_name TEXT,
    client_email TEXT
)
""")
conn.commit()

# Insert sample class if empty
cursor.execute("SELECT COUNT(*) FROM classes")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO classes (name) VALUES ('Yoga')")
    conn.commit()

# Timezone setup
timezone = pytz.timezone('Asia/Kolkata')

# In-memory schedule
fitness_classes = {
    "1": {
        "name": "Yoga",
        "datetime": timezone.localize(datetime(2025, 6, 10, 10, 0)),
        "instructor": "Anita",
        "slots": 5
    },
    "2": {
        "name": "Zumba",
        "datetime": timezone.localize(datetime(2025, 6, 11, 17, 0)),
        "instructor": "Rahul",
        "slots": 3
    },
    "3": {
        "name": "HIIT",
        "datetime": timezone.localize(datetime(2025, 6, 12, 7, 0)),
        "instructor": "Sneha",
        "slots": 2
    }
}

# GET /classes
@app.route('/classes', methods=['GET'])
def get_classes():
    user_tz = request.args.get('tz', 'Asia/Kolkata')
    try:
        target_tz = pytz.timezone(user_tz)
    except pytz.UnknownTimeZoneError:
        return jsonify({"error": "Invalid timezone"}), 400

    class_list = []
    for class_id, details in fitness_classes.items():
        localized_dt = details['datetime'].astimezone(target_tz)
        class_list.append({
            "id": class_id,
            "name": details["name"],
            "datetime": localized_dt.strftime('%Y-%m-%d %H:%M:%S %Z'),
            "instructor": details["instructor"],
            "slots": details["slots"]
        })
    return jsonify(class_list)

# POST /book
@app.route('/book', methods=['POST'])
def book_class():
    data = request.json
    class_id = data.get("class_id")
    name = data.get("client_name")
    email = data.get("client_email")

    if not all([class_id, name, email]):
        return jsonify({"error": "Missing required fields"}), 400

    cls = fitness_classes.get(class_id)
    if not cls:
        return jsonify({"error": "Invalid class ID"}), 404

    if cls["slots"] <= 0:
        return jsonify({"error": "Class is full"}), 400

    cls["slots"] -= 1

    # ✅ Insert booking into DB
    cursor.execute("""
    INSERT INTO bookings (class_id, client_name, client_email)
    VALUES (?, ?, ?)
    """, (class_id, name, email))
    conn.commit()

    return jsonify({"message": "Booking successful"})

# GET /bookings?client_email=someone@example.com
@app.route('/bookings', methods=['GET'])
def get_bookings():
    email = request.args.get("client_email")
    if not email:
        return jsonify({"error": "Email required"}), 400

    cursor.execute("SELECT class_id, client_name, client_email FROM bookings WHERE client_email = ?", (email,))
    results = cursor.fetchall()

    bookings_list = [
        {"class_id": row[0], "client_name": row[1], "client_email": row[2]}
        for row in results
    ]

    return jsonify(bookings_list)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
