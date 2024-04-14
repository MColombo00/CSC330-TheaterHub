import sqlite3
from app import db
from app import User
from app import Admin


def verify_login(email, user_password):
    user_email = User.query.filter_by(email_address=email).first()
    
    if email and user_email.password == user_password:
        return redirect(url_for('landing_page'))
    else:
        return 'Incorrect Email or Password'
    
def admin_verify(email, admin_password):
    admin_email = Admin.query.filter_by(email_address=email).first()
    if email and admin_email.password == admin_password:
        return redirect(url_for('landing_page'))
    else:
        return 'Incorrect Email or Password'
    
def forgot_password():
    return redirect(url_for('password_reset'))
