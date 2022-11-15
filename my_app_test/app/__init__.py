from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.app_context().push()

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://tuoi:12345678@localhost/TUOI_DB?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = 'agsjsskskcbdkdn'
app.config['UPLOAD_FOLDER'] = 'static/files'
db = SQLAlchemy(app=app)
# db.metadata.clear()

bootstrap = Bootstrap(app)

from app import models

