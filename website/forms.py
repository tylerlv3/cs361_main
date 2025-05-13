from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
import re


class CheckUserForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Invalid email address"),
        Length(max=120)
    ])
    submit = SubmitField('Continue')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Invalid email address"),
        Length(max=120)
    ])
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=50),
        Regexp(r'^[A-Za-z\s\-]+$', message="Name must contain only letters, spaces, or hyphens")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Invalid email address"),
        Length(max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters")
    ])
    submit = SubmitField('Log in') 