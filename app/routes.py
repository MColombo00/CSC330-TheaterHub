from app import app
from flask import Flask, render_template, redirect, url_for, request, jsonify
from app.forms import AddForm, DeleteForm, SearchForm
from app import db
import sys
import sqlite3
import json
from flask import session

api_key = 'eb6763dcd081514c5d528c58c863dd95'

# Load the JSON data once when the application starts
with open('MovieLocationScraper/Data Files/AMC/amc-movies.json', 'r') as file:
    movie_data = json.load(file)

def get_db_connection():
    conn = sqlite3.connect('profiles.db')
    return conn

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/buy_tickets')
def buy_tickets_page():
    return render_template('buy_tickets.html')

@app.route('/search_movie', methods=['GET'])
def search_movie():
    query = request.args.get('query')
    if query:
        results = [movie for movie in movie_data if query.lower() in movie['movie'].lower()]
        return render_template('search_results.html', query=query, results=results)
    else:
        return render_template('search_results.html', query=query, results=[])

@app.route('/cart')
def cart():
    movie = request.args.get('movie')
    time = request.args.get('time')
    location = request.args.get('location')
    theater = request.args.get('theater')

    # Store data in session
    session['movie'] = movie
    session['time'] = time
    session['location'] = location
    session['theater'] = theater

    return render_template('cart.html', movie=movie, time=time, location=location, theater=theater)

@app.route('/order_success', methods=['POST'])
def order_success():
    # Retrieve data from session
    movie = session.get('movie')
    time = session.get('time')
    location = session.get('location')
    theater = session.get('theater')

    return render_template('order_success.html', movie=movie, time=time, location=location, theater=theater)

@app.route('/profile')
def profile():
    if 'email' in session:  # Assuming the email is stored in the session
        email = session['email']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT genre FROM user_genres WHERE email_address=?', (email,))
        genres = [row[0] for row in cursor.fetchall()]
        conn.close()
        return render_template('profile.html', genres=genres)
    else:
        return redirect('/log_in')

@app.route('/change_genres')
def change_genres():
    return render_template('change_genres.html')

@app.route('/update_genres', methods=['POST'])
def update_genres():
    if 'email' in session:  # Assuming the email is stored in the session
        email = session['email']
        selected_genres = request.form.getlist('genres')
        conn = get_db_connection()
        cursor = conn.cursor()
        # Delete existing genres for the user
        cursor.execute('DELETE FROM user_genres WHERE email_address=?', (email,))
        # Insert selected genres into user_genres table
        for genre in selected_genres:
            cursor.execute('INSERT INTO user_genres (email_address, genre) VALUES (?, ?)', (email, genre))
        conn.commit()
        conn.close()
        # Redirect the user back to the profile page
        return redirect('/profile')
    else:
        return redirect('/log_in')

@app.route('/contact_us')
def contact_us_page():
    return render_template('contact_us.html')

@app.route('/log_in')
def log_in_page():
    error_message = request.args.get('error')
    return render_template('log_in.html', error=error_message)

@app.route('/admin_login')
def admin_login_page():
    error_message = request.args.get('error')
    return render_template('admin_login.html', error=error_message)

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
    genres = request.form.getlist('genre')  # Retrieve selected genres as a list

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
        
        # Retrieve the user_id of the newly inserted user
        cursor.execute('SELECT email_address FROM users WHERE email_address=?', (email,))
        email_address = cursor.fetchone()[0]  # Get the email_address of the newly inserted user

        # Insert selected genres into user_genres table
        for genre in genres:
            cursor.execute('INSERT INTO user_genres (email_address, genre) VALUES (?, ?)', (email_address, genre))

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

@app.route('/admin_login_handler', methods=['POST'])
def admin_login():
    email = request.form.get('email')
    inputted_password = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM admins WHERE email_address=?', (email,))
    admin = cursor.fetchone()
    if admin:
        password = admin[1]
        if password == inputted_password:
            session['admin_logged_in'] = True
            session['email'] = email
            session['password'] = password
            return redirect(url_for('landing_page'))

    error_message = 'Incorrect E-mail or Password.'
    return redirect(url_for('admin_login_page', error=error_message))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('landing_page'))

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
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

@app.route('/add_movie')
def add_movie():
    return render_template('add_movie.html')

@app.route('/add_movie_handler', methods=['POST'])
def input_movie():
    title = request.form.get('title')
    director = request.form.get('director')
    release_year = request.form.get('release_year')
    genre1 = request.form.get('genre1')
    genre2 = request.form.get('genre2')

    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM movies WHERE title=?', (title,))
    movie = cursor.fetchone()

    if movie:
        conn.close()
        error_message = 'This movie is already in the database.'
        return redirect(url_for('add_movie', error=error_message))
    else:
        cursor.execute('INSERT INTO movies (title, director, release_year,  genre1, genre2) VALUES (?, ?, ?, ?, ?)', (title, director, release_year, genre1, genre2))
        conn.commit()

        conn.close()
        error_message = 'Movie added to the database.'
        return redirect(url_for('add_movie', error=error_message))
        
@app.route('/delete_movie')
def delete_movie():
    return render_template('delete_movie.html')

@app.route('/delete_movie_handler', methods=['POST'])
def remove_movie():
    inputted_title = request.form.get('title')
    inputted_director = request.form.get('director')
    inputted_year = request.form.get('release_year')

    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM movies WHERE title=?', (inputted_title,))
    movie = cursor.fetchone()

    if movie:
        title = movie[0]
        director = movie[1]
        release_year = movie[2]
        if title == inputted_title:
            cursor.execute('DELETE FROM movies WHERE title=? AND director=? AND release_year=?', (inputted_title, director, inputted_year))
            conn.commit()
            conn.close()
            error_message = 'Movie removed from database.'
            return redirect(url_for('delete_movie', error=error_message))
    else:
        conn.close()
        error_message = 'This movie is not in the database.'
        return redirect(url_for('delete_movie', error=error_message))
