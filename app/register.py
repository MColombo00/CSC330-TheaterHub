import sqlite3

conn = sqlite3.connect('profiles.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS user
                (email_address TEXT NOT NULL,
                password NOT NULL)''')

def register_user(email, user_password):
    cursor.execute('SELECT * FROM users WHERE email_address=?', email)
    user = cursor.fecthone()
    if user:
        return 'An account using this email address already exists'
    else:
        cursor.execute('INSERT INTO user (email_address, password) VALUES (?, ?)',(email, user_password))

conn.commit()
conn.close()
