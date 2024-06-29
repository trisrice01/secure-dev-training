import os
from flask import Flask, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__, static_folder="./static")

app.config["SECRET_KEY"] = "1234"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'app.db')

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)

from app.models.user import User
from app.models.rdp_server import RDPServer

from .admin.routes import admin_bp
from .developer.routes import developer_bp
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(developer_bp, url_prefix="/developer")

from .utils import load_predefined_rdps

with app.app_context():
    load_predefined_rdps(db)

@login.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.context_processor
def utility_processor():
    return {
        "get_flashed_messages": get_flashed_messages
    }