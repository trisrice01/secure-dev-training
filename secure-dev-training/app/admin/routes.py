from flask import Blueprint, jsonify, request, render_template, redirect, flash, get_flashed_messages
from flask_login import current_user, login_user, login_required
from .forms import LoginForm, AddRDPServersForm, DeleteUserForm, MCQForm, ReorderMCQForm
from app.models.user import User
from app.models.rdp_server import RDPServer
from app.models.challenge import Challenge
from app.models.mcq import QuestionChoice, Question
from app.models.modules import Module
from app.models.code_challenge import CodeChallenge
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
    available_mcqs = Question.query.order_by(Question.order).all()
    available_modules = Module.query.all()
    available_code_challenges = CodeChallenge.query.all()
    login_code = login_code_service.get_login_code()
    return render_template(
        "admin_profile.html",
        add_rdp_form=form,
        available_rdp_servers=available_rdp_servers,
        available_challenges=available_challenges,
        available_mcqs=available_mcqs,
        available_modules=available_modules,
        available_code_challenges=available_code_challenges,
        login_code=login_code 
    )

@admin_bp.route("/toggle-enable", methods=["GET"])
@login_required
def module_enable():
    if not current_user or not current_user.is_admin:
        return redirect("/admin/login")

    module_id = request.args.get("id")

    if not module_id:
        return redirect("/admin")
    
    module = Module.query.get(module_id)
    module.is_enabled = not module.is_enabled
    db.session.add(module)
    db.session.commit()
    return redirect("/admin")

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

    if form.validate_on_submit():
        print([choice.is_correct.data for choice in form.choices])
        print(any([choice.is_correct for choice in form.choices]))
        if not any([choice.is_correct.data for choice in form.choices]):
            flash("At least one choice must be correct")
            print("INVALID INVALID")
            return render_template("admin_mcqs.html", form=form)

        mcq_question = Question()
        mcq_question.question_text = form.question_text.data
        db.session.add(mcq_question)
        db.session.commit()

        for choice in form.choices:
            mcq_choice = QuestionChoice()
            mcq_choice.choice_text = choice.choice_text.data
            mcq_choice.is_correct = choice.is_correct.data
            mcq_choice.question_id = mcq_question.id
            db.session.add(mcq_choice)
        db.session.commit()
        return redirect("/admin")

    return render_template("admin_mcqs.html", form=form, get_flashed_messages=get_flashed_messages)

@admin_bp.route("/mcq/view")
@login_required
def test():
    questions = Question.query.all()
    print(questions)
    for question in questions:
        for choice in question.question_choices:
            print(choice.is_correct)
        print(question.is_multi_choice)
    return ""

@admin_bp.route("/mcq/delete", methods=["POST"])
@login_required
def delete_mcq():
    mcq_id = request.form.get("mcq_id")
    question = Question.query.get(mcq_id)
    print(question)
    for choice in question.question_choices:
        db.session.delete(choice)
    db.session.delete(question)
    db.session.commit()
    return redirect("/admin")

@admin_bp.route("/mcq/reorder", methods=["POST"])
@login_required
def reoder_mcqs():
    request_json = request.get_json(force=True, silent=True)

    if not request_json:
        return jsonify({
            "error": True,
            "message": "Invalid JSON"
        })

    form: ReorderMCQForm = ReorderMCQForm.from_json(request_json)

    if not form.validate_on_submit():
        return {"success": False, "message": "Invalid form"}, 400
    
    for reordering in form.reordering:
        mcq_id = reordering.mcq.data
        order = reordering.order.data

        question = Question.query.get(mcq_id)
        question.order = order
        db.session.add(question)
    db.session.commit()
        
    return {
        "success": True
    }
