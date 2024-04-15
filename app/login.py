import sqlite3

conn = sqlite3.connect('profiles.db')
cursor = conn.cursor()

def user_login(email, user_password):
    cursor.execute('SELCT * FROM users WHERE email_address=?', (email,))
    user = cursor.fetchone()
    if user:
        password = user[1]
        if password == user_password:
            return 'Signed in'
        else:
            return 'Incorrect Email or Password'
    else:
        return 'Incorrect Email or Password'
    
def admin_verify(email, admin_password):
    cursor.execute('SELECT * FROM admins WHERE email_address=?', (email,))
    admin = cursor.fetchone()
    if email
        password = admin[1]
        if password == admin_password:
            return 'Signed in'
        else:
            'Incorrect Email or Password'
    else:
        return 'Incorrect Email or Password'
    
def forgot_password():
    return redirect(url_for('password_reset'))
