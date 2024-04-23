from app import app
from flask import Flask, render_template, redirect, url_for, request, jsonify
from app.forms import AddForm, DeleteForm, SearchForm
from app import db
import sys
import sqlite3
from flask import session

api_key = 'eb6763dcd081514c5d528c58c863dd95'

def get_db_connection():
    conn = sqlite3.connect('profiles.db')
    return conn

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/buy_tickets')
def buy_tickets_page():
    return render_template('buy_tickets.html')

@app.route('/cart')
def cart_page():
    return render_template('cart.html')

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/contact_us')
def contact_us_page():
    return render_template('contact_us.html')

@app.route('/log_in')
def log_in_page():
    error_message = request.args.get('error')
    return render_template('log_in.html', error=error_message)

@app.route('/admin_login')
def admin_login_page():
    return render_template('admin_login.html')

@app.route('/register')
def register_page():
    error_message = request.args.get('error')
    return render_template('register.html', error=error_message)

@app.route('/delete_account')
def delete_account_page():
    return render_template('delete_account.html')

@app.route('/change_email')
def change_email_page():
    return render_template('change_email.html')

@app.route('/update_password')
def update_password_page():
    return render_template('update_password.html')

@app.route('/reset_password')
def reset_password_page():
    return render_template('reset_password.html')

@app.route('/register_handler', methods=['POST'])
def register_handler():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        error_message = 'Passwords do not match'
        return redirect(url_for('register_page', error=error_message))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE email_address=?', (email,))
    user = cursor.fetchone()

    if user:
        conn.close()
        error_message = 'An account using this e-mail address already exists.'
        return redirect(url_for('register_page', error=error_message))
    else:
        cursor.execute('INSERT INTO users (email_address, password) VALUES (?, ?)', (email, password))
        conn.commit()

        conn.close()
        return redirect('/log_in')

@app.route('/login_handler', methods=['POST'])
def user_login():
    email = request.form.get('email')
    inputted_password = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email_address=?', (email,))
    user = cursor.fetchone()
    if user:
        password = user[1]
        if password == inputted_password:
            session['logged_in'] = True  # Set session variable
            session['email'] = email  # Store email in session
            session['password'] = password  # Store password in session
            return redirect(url_for('landing_page'))
    
    error_message = 'Incorrect E-mail or Password.'
    return redirect(url_for('log_in_page', error=error_message))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('landing_page'))

@app.route('/change_email_handler', methods=['POST'])
def change_email():
    inputted_email = request.form.get('email')
    new_email = request.form.get('new_email')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email_address=?', (inputted_email,))
    user = cursor.fetchone()

    if user:
        email = user[0]
        if email == inputted_email:
            cursor.execute('UPDATE users SET email_address=? WHERE email_address=?', (new_email, inputted_email))
            conn.commit()
            conn.close()
            return redirect(url_for('profile_page'))
    
    error_message = 'Incorrect email.'
    return redirect(url_for('update_password_page', error=error_message))

@app.route('/update_password_handler', methods=['POST'])
def update_password():    
    inputted_password = request.form.get('password')
    new_password = request.form.get('new_password')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE password=?', (inputted_password,))
    user = cursor.fetchone()

    if user:
        password = user[1]
        if password == inputted_password:
            cursor.execute('UPDATE users SET password=? WHERE password=?', (new_password, inputted_password))
            conn.commit()
            conn.close()
            return redirect(url_for('profile_page'))
    
    error_message = 'Incorrect password.'
    return redirect(url_for('update_password_page', error=error_message))

@app.route('/reset_password_handler', methods=['POST'])
def reset_password():
    #implement password reset

    return redirect(url_for('profile_page'))

@app.route('/delete_account_handler', methods=['POST'])
def delete_account():
    inputted_email = request.form.get('email')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email_address=?', (inputted_email,))
    user = cursor.fetchone()

    if user:
        email = user[0]
        if email == inputted_email:
            cursor.execute('DELETE FROM users WHERE email_address=?', (inputted_email,))
            conn.commit()
            conn.close()
            return redirect(url_for('logout'))