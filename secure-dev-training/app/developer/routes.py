from flask import Blueprint, request, render_template, redirect, flash, get_flashed_messages
from flask_login import current_user, login_user, login_required
from app.models.user import User
from app.models.rdp_server import RDPServer
from app import db
import bcrypt
from .forms import RegisterForm, LoginForm


developer_bp = Blueprint("developer", __name__, template_folder="./templates")

@developer_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        u = User.query.filter_by(username=username).first()
        if u:
            flash("That username is already taken!", "error")
            return render_template("register.html", form=form)
        
        user_rdp_server = RDPServer.query.filter_by(is_taken=False).first()
        user_rdp_server.is_taken = True
        u = User()
        u.rdp_server = user_rdp_server
        u.username = form.username.data
        u.password = bcrypt.hashpw(form.password.data.encode(), salt=bcrypt.gensalt())
        db.session.add(u)
        db.session.add(user_rdp_server)
        db.session.commit()
        login_user(u)
        return redirect("/developer/")
    return render_template("register.html", form=form)

@developer_bp.route("/login", methods=["GET", "POST"])
def login():
    form: LoginForm = LoginForm()

    if not form.validate_on_submit():
        return render_template("login.html", form=form)
    
    u = User.query.filter_by(username=form.username.data).first()

    if not u or not u.verify_password(form.password.data):
        flash("Invalid username or password", "error")
        return render_template("register.html", form=form)

    return redirect("/developer/")
    
@developer_bp.route("/")
@login_required
def dev_index():
    rdp_server = current_user.rdp_server_connection
    return render_template("rdp.html", rdp_server=rdp_server)