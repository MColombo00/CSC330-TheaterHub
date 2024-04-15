import sqlite3

conn = sqlite3.connect('profiles.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (email_address TEXT NOT NULL,
                password TEXT NOT NULL)''')

def register_user(email, user_password):
    cursor.execute('SELECT * FROM users WHERE email_address=?', (email,))
    user = cursor.fetchone()
    if user:
        return 'An account using this email address already exists'
    else:
        cursor.execute('INSERT INTO user (email_address, password) VALUES (?, ?)',(email, user_password))
        conn.commit
        
conn.close()
