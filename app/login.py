import sqlite3

conn = sqlite3.connect('profiles.db')
cursor = conn.cursor()

def user_login(email, user_password):
    cursor.execute('SELCT * FROM users WHERE email_address=?', email)
    user = cursor.fetchone()
    password = user[1]
    
    if email and password == user_password:
        return 'Sign in'
    else:
        return 'Incorrect Email or Password'
    
def admin_verify(email, admin_password):
    cursor.execut('SELECT * FROM admins WHERE email_address=?', email)
    admin = cursor.fetchone()
    password = admin[1]

    if email and password == admin_password:
        return 'sign in'
    else:
        return 'Incorrect Email or Password'
    
def forgot_password():
    return redirect(url_for('password_reset'))
