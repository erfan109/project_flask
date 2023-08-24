from market.forms import RegisterForm , LoginForm , Item_form , PurchaseItemForm , SellItemForm
from market.models import Item , User
from market import app
from flask import render_template , redirect , url_for , flash , request , get_flashed_messages
from market import db
from flask_login import login_user , logout_user , login_required , current_user
ADMIN_ACCESS = False

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")


@app.route('/Market',methods = ["GET","POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sellForm = SellItemForm()
    if request.method == "POST":
        purchase_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name = purchase_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                
                flash(f"Congratulations! you have purchased {p_item_object.name} for {p_item_object.Price}$",category = "success")
            else:
                flash(f"Unfortunately you dont have the credits to buy {p_item_object.name}", category="danger")


        sold_item = request.form.get("sold_item")
        s_item_obj=Item.query.filter_by(name = sold_item).first()
        if s_item_obj:
            if current_user.can_sell(s_item_obj):
                s_item_obj.sell(current_user)
                flash(f"Congratulations! you have Sold {s_item_obj.name}",category = "success")
            else:
                flash(f"Unfortunately you dont own this item {s_item_obj.name}", category="danger")

        return redirect(url_for("market_page"))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owend_items = Item.query.filter_by(owner = current_user.id)
        return render_template('market.html',items = items , purchase_form=purchase_form,owend_items=owend_items , sellForm = sellForm)


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
        attempted_user = user_to_create
        login_user(attempted_user)
        flash(f"logging attempt was Successful you are now logged in as : {attempted_user.username}",category="success")
        return redirect(url_for('market_page'))
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