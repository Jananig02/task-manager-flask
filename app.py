from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "taskmanagersecret"

# DATABASE SETUP
def init_db():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    ''')

    # TASKS TABLE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        status TEXT,
        user_id INTEGER
    )
    ''')

    conn.commit()
    conn.close()

# INITIALIZE DATABASE
init_db()

# HOME
@app.route('/')
def home():
    return redirect('/login')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session['user_id'] = user[0]

            return redirect('/dashboard')

        else:
            return "Invalid Username or Password"

    return render_template('login.html')

# DASHBOARD
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    # CHECK LOGIN
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # ADD TASK
    if request.method == 'POST':

        title = request.form['task']
        status = request.form['status']

        user_id = session['user_id']

        cursor.execute(
            "INSERT INTO tasks (title, status, user_id) VALUES (?, ?, ?)",
            (title, status, user_id)
        )

        conn.commit()

    # FETCH ONLY LOGGED-IN USER TASKS
    cursor.execute(
        "SELECT * FROM tasks WHERE user_id=?",
        (session['user_id'],)
    )

    tasks = cursor.fetchall()

    conn.close()

    return render_template('dashboard.html', tasks=tasks)

# DELETE TASK
@app.route('/delete/<int:id>')
def delete_task(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')

# UPDATE TASK STATUS
@app.route('/update/<int:id>/<status>')
def update_status(id, status):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (status, id)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')

# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

# RUN APP
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)