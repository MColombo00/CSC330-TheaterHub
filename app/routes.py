from app import app
from flask import Flask, render_template, redirect, url_for, request, jsonify
from app.forms import AddForm, DeleteForm, SearchForm
from app import db
import sys
import sqlite3

api_key = 'eb6763dcd081514c5d528c58c863dd95'

def get_db_connection():
    conn = sqlite3.connect('profiles.db')
    conn.row_factory = sqlite3.Row
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
    return render_template('log_in.html')

@app.route('/admin_login')
def admin_login_page():
    return render_template('admin_login.html')

@app.route('/register')
def register_page():
    error_message = request.args.get('error')
    return render_template('register.html', error=error_message)

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