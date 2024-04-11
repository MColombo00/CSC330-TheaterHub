from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class AddForm(FlaskForm):
    user_id = StringField('User ID:', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number: ', validators=[DataRequired()])
    email_address = IntegerField('Email Address: ', validators=[DataRequired()])
    password = IntegerField('Password: ', validators=[DataRequired()])
    favorite_genre = IntegerField('Favorite Genre: ', validators=[DataRequired()])
    submit = SubmitField('Save')
 
class DeleteForm(FlaskForm):
    user_id = StringField('User ID:', validators=[DataRequired()])
    submit = SubmitField('Delete')

class SearchForm(FlaskForm):
    user_id = StringField('User ID:', validators=[DataRequired()])
    submit = SubmitField('Search')
