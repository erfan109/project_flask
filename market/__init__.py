from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///market.db"
app.config["SECRET_KEY"] = '60de51371c4554b676e11700'
db = SQLAlchemy(app)
from market import route

app.app_context().push()

