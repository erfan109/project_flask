from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import Length , EqualTo , Email , DataRequired , ValidationError
from market.models import User

class RegisterForm(FlaskForm):


    def validate_username(self,username_to_check):
        user = User.query.filter_by(username = username_to_check.data).first()
        if user:
            raise ValidationError("username already exists ! try using another Username")
        
    def validate_email_adress(self,email_to_check):
        email = User.query.filter_by(email_address = email_to_check.data).first()
        if email:
            raise ValidationError("Email address already exists try anoher Email")
        
    username = StringField(label="User Name", validators = [Length(min=2,max=30),DataRequired()])
    email_adress = StringField(label="Email Adress", validators = [Email(),DataRequired()])
    password1 = PasswordField(label="Password", validators = [Length(min=8),DataRequired()])
    password2 = PasswordField(label="Repeat Your Password", validators = [EqualTo('password1'),DataRequired()])
    submit = SubmitField(label="Submit your information")