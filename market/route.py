from market.forms import RegisterForm , LoginForm
from market.models import Item , User
from market import app
from flask import render_template , redirect , url_for , flash , get_flashed_messages
from market import db



@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

@app.route('/Market')
def market_page():
    items = Item.query.all()
    return render_template('market.html',items = items)

@app.route('/register',methods = ["GET","POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                              email_address = form.email_adress.data,
                              password = form.password1.data,
                              )
        db.session.rollback()
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"there was an error with your information {err}",category="danger")

    return render_template('register.html',form = form)

@app.route('/login',methods = ["GET","POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username5 = form.username.data
        password5 = form.password.data
        user = User.query.filter_by(username = username5).first()
        user_password = User.query.filter_by(password_hash = password5).first()
        if user and user_password:
            return redirect(url_for('market_page')) 
    return render_template('login.html',form=form)
