from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    # table name (overridden)
    __tablename__ = 'user'

    # columns of table
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    # customer_id = db.relationship('Customer', backref='user', lazy='dynamic')
    pending_pay = db.relationship('Ppay', backref='user', lazy='dynamic')
    pay_history = db.relationship('Hpay', backref='user', lazy='dynamic')

    def __init__(self, firstname, lastname, email, username, password, is_admin):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)  # hashed the password
        self.is_admin = is_admin

    # function to check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Ppay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100))
    total_amount = db.Column(db.Integer, nullable=True)
    paid_amount = db.Column(db.Integer, nullable=True)
    pending_amount = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __init__(self, product, total_amount, paid_amount, pending_amount, user_id):
        self.product = product
        self.total_amount = total_amount
        self.paid_amount = paid_amount
        self.pending_amount = pending_amount
        self.user_id = user_id


class Hpay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_email = db.Column(db.String(200))
    product = db.Column(db.String(200))
    amount = db.Column(db.Integer, nullable=True)
    closed_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __init__(self, customer_email, product, amount, user_id):
        self.customer_email = customer_email
        self.product = product
        self.amount = amount
        self.user_id = user_id

