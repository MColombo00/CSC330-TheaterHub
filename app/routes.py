from app import app
from flask import render_template, redirect, url_for
from app.forms import AddForm, DeleteForm, SearchForm
from app import db
import sys

api_key = 'eb6763dcd081514c5d528c58c863dd95'

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

# Not implemented yet
#@app.route('/register')
#def admin_login_page():
#    return render_template('admin_login.html')


#The below code we can use for reference, but is unnecessary.
#DELETE WHEN UNNEEDED.
@app.route('/add', methods=['GET', 'POST'])
def add_record():
    form = AddForm()
    if form.validate_on_submit():
        # Extract values from form
        city_name = form.city.data
        population = form.population.data

        # Create a city record to store in the DB
        c = City(city=city_name, population=population)

        # add record to table and commit changes
        db.session.add(c)
        db.session.commit()

        form.city.data = ''
        form.population.data = ''
        return redirect(url_for('add_record'))
    return render_template('add.html', form=form)

@app.route('/delete', methods=['GET', 'POST'])
def delete_record():
    form = DeleteForm()
    if form.validate_on_submit():
        # Query DB for matching record (we'll grab the first record in case
        # there's more than one).
        to_delete = db.session.query(City).filter_by(city = form.city.data).first()

        # If record is found delete from DB table and commit changes
        if to_delete is not None:
            db.session.delete(to_delete)
            db.session.commit()

        form.city.data = ''
        # Redirect to the view_all route (view function)
        return redirect(url_for('view'))
    return render_template('delete.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search_by_name():
    form = SearchForm()
    if form.validate_on_submit():
        # Query DB table for matching name
        record = db.session.query(City).filter_by(city = form.city.data).all()
        if record:
            return render_template('view_cities.html', cities=record)
        else:
            return render_template('not_found.html')
    return render_template('search.html', form=form)

@app.route('/view_all')
def view():
    all = db.session.query(City).all()
    print(all, file=sys.stderr)
    return render_template('view_cities.html', cities=all)

@app.route('/sort_by_name')
def sort_by_name():
    all = db.session.query(City).order_by(City.city).all()
    print(all, file=sys.stderr)
    return render_template('view_cities.html', cities=all)
