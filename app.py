from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('login.html')


# Connect to the SQLite database
conn = sqlite3.connect('users.db')

# Define a function to authenticate user credentials
def authenticate(username, password):
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    if result is not None:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if hashed_password == result[0]:
            return True
    return False

# Define the signup view function
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        password = request.form['password']
        # Hash the password
        hashed_password = hash_password(password)
        # Insert the new user information into the database
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        # Redirect to the login page
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

# Define the login view function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Authenticate the user
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        if result is not None:
            hashed_password = hash_password(password)
            if hashed_password == result[0]:
                return redirect(url_for('dashboard'))
        error = 'Invalid username or password'
        return render_template('login.html', error=error)
    else:
        return render_template('login.html')