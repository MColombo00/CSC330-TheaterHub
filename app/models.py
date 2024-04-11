from app import db

# Database Classes
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.String(64), primary_key=True)
    phone_number= db.Column(db.String(64), unique=False, nullable=False)
    email_address = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), unique=False, nullable=False)
    favorite_genre = db.Column(db.String(64), unique=False, nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    phone_number= db.Column(db.String(64), unique=False, nullable=False)
    email_address = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), unique=False, nullable=False)

    def __repr__(self):
        return self.user_id + ': ' + str(self.email_address)
