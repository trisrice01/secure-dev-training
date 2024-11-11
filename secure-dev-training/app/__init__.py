import os
from flask import Flask, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import wtforms_json
from dotenv import load_dotenv


app = Flask(__name__, static_folder="./static")
load_dotenv()

app.config["SECRET_KEY"] = "1234"
basedir = os.path.abspath(os.path.dirname(__file__))

db_filename = os.getenv("DB_FILENAME") or "app.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, db_filename)

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)

from .services import LoginCodeService

login_code_service = LoginCodeService.init_app(app, db)

# Services

wtforms_json.init()

from app.models.user import User
from app.models.rdp_server import RDPServer
from app.models.challenge import Challenge

from .admin.routes import admin_bp
from .developer.routes import developer_bp
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(developer_bp, url_prefix="/developer")

@login.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.context_processor
def utility_processor():
    return {
        "get_flashed_messages": get_flashed_messages
    }