import mysql.connector
from flask import request

# Connect to MySQL database
conn = mysql.connector.connect(
    host="db4free.net",
    user="personaltailr",
    password="personaltailr",
    database="personaltailr"
)
cursor = conn.cursor()

def create_tables():
    # Create 'customers' table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))")

def insert_data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']

        # Check if email already exists in the database
        cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
        user_data = cursor.fetchone()

        if not user_data:
            # Insert new user data into 'customers' table
            cursor.execute("INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            conn.commit()
            return True
        else:
            return False

def check_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        # Check if email and password match in the database
        cursor.execute("SELECT * FROM customers WHERE email = %s AND password = %s", (email, password))
        user_data = cursor.fetchone()

        if not user_data:
            return False, ""
        else:
            return True, user_data[1]  # Assuming the second column is 'name'

# Ensure tables exist before interacting with them
create_tables()
