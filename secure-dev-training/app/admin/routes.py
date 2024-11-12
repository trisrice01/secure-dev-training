from flask import Blueprint, jsonify, request, render_template, redirect, flash, get_flashed_messages
from flask_login import current_user, login_user, login_required
from .forms import LoginForm, AddRDPServersForm, DeleteUserForm, MCQForm
from app.models.user import User
from app.models.rdp_server import RDPServer
from app.models.challenge import Challenge
from .utils import is_valid_ip
from app import db
from .forms import ChangeLoginCodeForm
from app import login_code_service


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
    
    return render_template("admin_login.html", form=form)


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
    available_challenges = Challenge.query.all()
    login_code = login_code_service.get_login_code()
    return render_template(
        "admin_profile.html",
        add_rdp_form=form,
        available_rdp_servers=available_rdp_servers,
        available_challenges=available_challenges,
        login_code=login_code 
    )

@admin_bp.route("/change-login-code", methods=["POST"])
@login_required
def change_login_code():
    if not current_user or not current_user.is_admin:
        return redirect("/admin/login")
    
    request_json = request.get_json(force=True, silent=True)

    if not request_json:
        return jsonify({
            "error": True,
            "message": "Invalid JSON"
        })

    form = ChangeLoginCodeForm.from_json(request_json)

    if not form.validate():
        return jsonify({
            "error": True,
            "message": "Invalid form"
        })

    login_code_service.set_login_code(form.login_code.data)

    return jsonify({
        "success": True,
        "message": "Code updated!"
    })
    
@admin_bp.route("/delete-user", methods=["POST"])
@login_required
def delete_user():
    if not current_user or not current_user.is_admin:
        return redirect("/admin/login")

    request_json = request.get_json(force=True, silent=True)

    if not request_json:
        return jsonify({
            "error": True,
            "message": "Invalid JSON"
        })
    
    form = DeleteUserForm.from_json(request_json)
    if not form.validate():
        return jsonify({
            "error": True,
            "message": "Invalid form"
        })
    
    user_id = None
    try:
        user_id = int(form.user_id.data)
    except ValueError:
        return jsonify({
            "error": True,
            "message": "Invalid user id"
        })
    user = User.query.get(user_id)
    rdp_server = user.rdp_server
    rdp_server.user_id = None
    rdp_server.is_taken = False
    db.session.delete(user)
    db.session.add(rdp_server)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "User deleted successfully!"
    })


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

@admin_bp.route("/mcq", methods=["GET", "POST"])
@login_required
def mcq_management():
    if not current_user or not current_user.is_admin:
        return redirect("/admin/login")
    
    form = MCQForm()

    print(form.choices.data)
    print(form.question_text.data)
    if form.validate_on_submit():
        print(form)

    return render_template("admin_mcqs.html", form=form)