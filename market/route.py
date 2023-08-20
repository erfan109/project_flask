from market.forms import RegisterForm , LoginForm , Item_form
from market.models import Item , User
from market import app
from flask import render_template , redirect , url_for , flash , get_flashed_messages
from market import db
from flask_login import login_user , logout_user , login_required
ADMIN_ACCESS = False

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")


@app.route('/Market')
@login_required
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
        return redirect(url_for('login_page'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"there was an error with your information {err}",category="danger")
    return render_template('register.html',form = form)


@app.route("/admin",methods = ["GET","POST"])
@login_required
def admin_page():
    form = Item_form()
    if form.validate_on_submit():
        item_to_create = Item(
            name = form.product_name.data,
            Price = int(form.product_price.data),
            description = form.product_description.data,
            barcode = form.product_barcode.data,
                            )
        db.session.add(item_to_create)
        db.session.commit()
    return render_template("admin.html",form=form)






@app.route('/login',methods = ["GET","POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user.username == "admin1" and attempted_user.check_password_correction(attempted_password=form.password.data):
            ADMIN_ACCESS = True
            if ADMIN_ACCESS:
                login_user(attempted_user)
                flash(f"wellcome Admin",category="success")
                return redirect(url_for('admin_page'))
        elif attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
           login_user(attempted_user)
           flash(f"logging attempt was Successful you are now logged in as : {attempted_user.username}",category="success")
           return redirect(url_for('market_page'))
        
        

        else:
            flash("username or password is inccorect!!",category="danger")
    return render_template('login.html',form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("you have been logged out of your account Succsefuly",category="info")
    return redirect(url_for("home_page"))