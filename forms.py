from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField, IntegerField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, Length




class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=3, max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20, message='Username must be min 4 to max 20 characters!')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddPaymentForm(FlaskForm):
    product = StringField('Product', validators=[DataRequired()])
    paid_amount = IntegerField('Paid Amount', validators=[DataRequired()])
    total_amount = IntegerField('Total Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MessageForm(FlaskForm):
    messages = TextAreaField('Messages', validators=[Length(max=200)])
    submit = SubmitField('Send')