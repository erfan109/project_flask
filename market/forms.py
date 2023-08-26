from django.forms import IntegerField
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


class LoginForm(FlaskForm):
    username = StringField(label="Username",validators=[DataRequired()])
    password = PasswordField(label="Password",validators=[DataRequired()])
    submit = SubmitField(label="Sign in")



class Item_form(FlaskForm):
    product_name = StringField(label="Product name",validators=[DataRequired()])
    product_barcode = StringField(label="Product barcode",validators=[DataRequired()])
    product_price = StringField(label="Product price",validators=[DataRequired()])
    product_description = StringField(label="Product discription",validators=[DataRequired()])
    submit = SubmitField(label="create item")
    

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase item")

class SellItemForm(FlaskForm):
    submit = SubmitField(label="Sell item")


