import sqlite3

# Function to connect to the SQLite database
def get_connection():
    """Establishes a connection to the SQLite database."""
    # The database file will be created in your project folder if it doesn't exist.
    conn = sqlite3.connect('user_data.db')
    return conn

# Function to create the 'users' table if it doesn't already exist
def create_usertable():
    """Creates the user table in the database to store registration info."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a new user's data to the table
def add_userdata(username, password):
    """Inserts a new user into the users table."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users(username, password) VALUES (?,?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # This error occurs if the username is already taken
        return False
    finally:
        conn.close()

# Function to verify a user's credentials during login
def login_user(username, password):
    """Checks if a username and password match a record in the database."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username =? AND password =?', (username, password))
    data = c.fetchall()
    conn.close()
    return data

