from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, IntegerField, DateTimeField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired, NumberRange
from datetime import datetime

# User Registration Form
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=80)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=120)])
    role = SelectField('Role', choices=[('delivery', 'Delivery'), ('user', 'User')], validators=[DataRequired()])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# User Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Update User Information Form
class UpdateUserForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=80)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=80)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=120)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=10)])
    submit = SubmitField('Update')

# Password Reset Form
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

# Forget Password Form
class ForgetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class AddItemForm(FlaskForm):
    """Form for adding items to the shop."""
    name = StringField('Name', validators=[DataRequired(message="Name is required.")])
    
    description = StringField('Description', validators=[DataRequired(message="Description is required.")])
    
    price = FloatField('Price', validators=[
        InputRequired(message="Price is required."),
        NumberRange(min=0, message="Price must be a positive number.")
    ])
    
    stock_quantity = IntegerField('Stock Quantity', validators=[
        InputRequired(message="Stock quantity is required."),
        NumberRange(min=0, message="Stock quantity must be a non-negative number.")
    ])
    
    brand = StringField('Brand', validators=[DataRequired(message="Brand is required.")])
    
    category = StringField('Category', validators=[DataRequired(message="Category is required.")])
    
    updated_at = DateTimeField('Updated At', default=datetime.utcnow)  # Optional, auto-populates with current time
    
    rating = FloatField('Rating', validators=[
        NumberRange(min=0, max=5, message="Rating must be between 0 and 5.")
    ])
    
    ratting = StringField('Ratting', validators=[DataRequired(message="Ratting is required.")])
