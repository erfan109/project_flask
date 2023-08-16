from market.forms import RegisterForm
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
                              password_hash = form.password1.data,
                              )
        db.session.rollback()
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"there was an error with your information {err}",category="danger")

    return render_template('register.html',form = form)


