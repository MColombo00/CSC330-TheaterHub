import sqlite3
from app import db
from app import User
import mysql.connector

user_db = mysql.connector.connect(
    host = 'localhost',
    user = 'username',
    password = 'password',
    database = 'User')

userCursor = user_db.cursor()

def register_user(email, user_password):
    user_email = User.query.filter_by(email_address=email).first()
    if email:
        return 'An account using this email address already exists'
    else:
        sql = "INSERT INTO user (email_address, password) VALUES (%s, %s)"
        val = [email, user_password]
        userCursor.executemany(sql,val)
        user_db.commit()

