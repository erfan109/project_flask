from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///market.db"

db = SQLAlchemy(app)


app.app_context().push()
with app.app_context():
    db.create_all()


