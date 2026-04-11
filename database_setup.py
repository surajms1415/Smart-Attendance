# database_setup.py
import sqlite3
import os

# Define the database name
DB_NAME = "attendance.db"

def create_database():
    """Creates the necessary tables if they don't exist."""
    
    # Check if the registered_faces directory exists, if not, create it
    if not os.path.exists("registered_faces"):
        os.makedirs("registered_faces")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create the 'employees' table
    # We will store face encodings as JSON text
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        face_encoding TEXT NOT NULL,
        image_path TEXT
    );
    ''')

    # Create the 'attendance' table
    # We use a composite primary key (employee_id, date) to ensure
    # one employee is marked only once per day.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        employee_id TEXT,
        date TEXT,
        status TEXT DEFAULT 'present',
        PRIMARY KEY (employee_id, date),
        FOREIGN KEY (employee_id) REFERENCES employees (id)
    );
    ''')

    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' and tables created successfully.")
    print("Please make sure you have a 'registered_faces' folder in this directory.")

if __name__ == "__main__":
    create_database()