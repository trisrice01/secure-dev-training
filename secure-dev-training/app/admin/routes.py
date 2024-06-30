from flask import Blueprint, request, render_template, redirect, flash, get_flashed_messages
from flask_login import current_user, login_user, login_required
from .forms import LoginForm, AddRDPServersForm
from app.models.user import User
from app.models.rdp_server import RDPServer
from .utils import is_valid_ip
from app import db


admin_bp = Blueprint("admin", __name__, template_folder="./templates")

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data, password=form.password.data, is_admin=True).first()
        if not u:
            return redirect("/admin/login")
        
        login_user(u)
        return redirect("/admin")
    
    return render_template("login.html", form=form)


@admin_bp.route("/testing")
def testing():
    rdp_servers_list = RDPServer.query.all()
    string = ""
    for rdp_server in rdp_servers_list:
        string += rdp_server.ip_addr + "\n"
    return string

@admin_bp.route("/", methods=["GET"])
@login_required
def admin():
    if not current_user or not current_user.is_admin:
        return redirect("/admin/login")
    form = AddRDPServersForm()
    available_rdp_servers = RDPServer.query.all()
    return render_template(
        "admin_profile.html",
        add_rdp_form=form,
        available_rdp_servers=available_rdp_servers
    )

@admin_bp.route("/add-rdp-servers", methods=["POST"])
@login_required
def add_rdp_servers():
    if not current_user or not current_user.is_admin:
        return redirect("/admin/login")
    
    form = AddRDPServersForm()

    if form.validate_on_submit():
        ip_addrs = form.rdp_servers.data.splitlines()
        for ip_addr in ip_addrs:
            if not is_valid_ip(ip_addr):
                flash(ip_addr, "invalid_ip")
            else:
                r = RDPServer()
                r.ip_addr = ip_addr
                db.session.add(r)
                db.session.commit()

    return redirect("/admin/")
    