import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd53157d4061ed102dae462d1365e8b11'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trip.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'
login_manager.login_message_category = 'info'

file_path = op.join(op.dirname(__file__), 'static/img/profilepic')
try:
    os.mkdir(file_path)
except OSError:
    pass

from travel import routes
from travel import admins
