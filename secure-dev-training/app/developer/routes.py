from flask import Blueprint, request, render_template, redirect, flash, jsonify
from flask_login import current_user, login_user, login_required
from app.models.user import User
from app.models.challenge import Challenge
from app.models.rdp_server import RDPServer
from app.models.user_challenge_completions import UserChallengeCompletions
from app import db
import bcrypt
from .forms import RegisterForm, LoginForm, ChallengeCompletionForm
from app import login_code_service


developer_bp = Blueprint("developer", __name__, template_folder="./templates")

@developer_bp.route("/me", methods=["GET"])
@login_required
def me():
    return login_code_service.get_login_code()

@developer_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash("Your passwords must be equal", "error")
            return render_template("register.html", form=form)
    
        username = form.username.data
        u = User.query.filter_by(username=username).first()
        if u:
            flash("That username is already taken!", "error")
            return render_template("register.html", form=form)
        
        user_rdp_server = RDPServer.query.filter_by(is_taken=False).first()
        if not user_rdp_server:
            flash("There are no more RDP servers available, please talk to the professor", "error")
            return render_template("register.html", form=form)
        
        login_code = login_code_service.get_login_code()

        if form.login_code.data != login_code:
            flash("Incorrect login code!", "error")
            return render_template("register.html", form=form)

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
        return render_template("developer_login.html", form=form)
    
    u = User.query.filter_by(username=form.username.data).first()

    if not u or not u.verify_password(form.password.data):
        flash("Invalid username or password", "error")
        return render_template("developer_login.html", form=form)

    login_user(u)
    return redirect("/developer/")
    
@developer_bp.route("/")
@login_required
def dev_index():
    rdp_server = current_user.rdp_server_connection
    challenges = Challenge.query.all()
    return render_template("rdp.html", rdp_server=rdp_server, challenges=challenges, current_user=current_user)

@developer_bp.route("/challenges", methods=["GET"])
@login_required
def list_challenges():
    all_challenges: list[Challenge] = Challenge.query.all()
    challenges_response = {
        "total": len(all_challenges),
        "challenges": [{
            "id": challenge.id,
            "ip": challenge.ip_addr,
            "name": challenge.name,
            "description": challenge.description,
            "is_complete": (current_user in challenge.completed_users)
        } for challenge in all_challenges]
    }
    return jsonify(challenges_response)

@developer_bp.route("/challenge/complete", methods=["POST"])
@login_required
def complete_challenge():
    request_json = request.get_json(force=True, silent=True)

    if not request_json:
        return jsonify({
            "error": True,
            "message": "Invalid JSON"
        })
    
    form: ChallengeCompletionForm = ChallengeCompletionForm.from_json(request_json)

    if not form.validate():
        return jsonify({
            "error": True,
            "message": "Invalid form"
        })

    challenge: Challenge = Challenge.query.get(form.challenge_id.data)
    if not challenge:
        return jsonify({
            "error": True,
            "message": "That challenge could not be found!"
        })
    
    if current_user in challenge.completed_users:
        return jsonify({
            "error": True,
            "message": "You have already completed this challenge!"
        })
    
    if challenge.flag != form.challenge_flag.data:
        return jsonify({
            "error": True,
            "message": "Invalid challenge flag"
        })
    
    challenge_completion = UserChallengeCompletions()
    challenge_completion.user_id = current_user.id
    challenge_completion.challenge_id = challenge.id

    db.session.add(challenge_completion)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Challenge completed successfully!"
    })