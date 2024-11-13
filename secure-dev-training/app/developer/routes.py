from flask import Blueprint, request, render_template, redirect, flash, jsonify
from flask_login import current_user, login_user, login_required
from app.models.user import User
from app.models.challenge import Challenge
from app.models.modules import Module
from app.models.code_challenge import CodeChallenge
from app.models.rdp_server import RDPServer
from app.models.user_challenge_completions import UserChallengeCompletions
from app.models.user_codechallenge_completions import UserCodeChallengeCompletions
from app import db
from app.models.mcq import Question, UserMCQCompletions
import bcrypt
from .forms import RegisterForm, LoginForm, ChallengeCompletionForm, CompleteMCQForm
from .forms import RegisterForm, LoginForm, ChallengeCompletionForm
from .codechallenge import add_code_challenges
from app import login_code_service
from .decorators.modules import module_enabled, MODULE_CODE, MODULE_CTF, MODULE_THEORY


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
    add_code_challenges()
    rdp_server = current_user.rdp_server_connection
    challenges = Challenge.query.all()
    return render_template("rdp.html", rdp_server=rdp_server, challenges=challenges, current_user=current_user)

@developer_bp.route("/home")
@login_required
def dev_home():
    modules = Module.query.all()
    return render_template("developer_home.html", modules=modules)

@developer_bp.route("/mcqs/next", methods=["GET", "POST"])
@login_required
@module_enabled(MODULE_THEORY)
def next_mcq():
    extraJson = {}
    if request.method == "POST":
        request_json = request.get_json(force=True, silent=True)

        if not request_json:
            return jsonify({
                "error": True,
                "message": "Invalid JSON"
            })


        form: ChallengeCompletionForm = CompleteMCQForm.from_json(request_json)

        if not form.validate():
            return jsonify({
                "error": True,
                "message": "Invalid form"
            })
        
        # Check if question exists
        question = Question.query.get(form.question_id.data)
        
        
        if not question:
            return jsonify({
                "error": True,
                "message": "Invalid question"
            }), 404
        
        completed_challenge = UserMCQCompletions.query.filter_by(
            user_id=current_user.id, question_id=form.question_id.data
        ).first()

        if completed_challenge:
            return jsonify({
                "error": True,
                "message": "You have already completed this challenge!"
            }), 400
        
        # Ensure that if more than 1 choice is submitted, the question is multi-choice

        if len(form.choice_ids) > 1 and not question.is_multi_choice:
            return jsonify({
                "error": True,
                "message": "This question does not have multiple answers"
            }), 400
        
        is_correct = True
        incorrect_choices = []
        question_choice_ids = {choice.id: choice for choice in question.question_choices}
        for choice_id in form.choice_ids.data:
            question_choice = question_choice_ids.get(choice_id)
            if not question_choice:
                is_correct = False
                continue
                # return jsonify({
                #     "error": True,
                #     "message": "Invalid choice"
                # })

            if not question_choice.is_correct:
                is_correct = False
                # incorrect_choices.append()
                # return jsonify({
                #     "error": True,
                #     "message": "Wrong choice",
                #     "correct_choice": [choice.id for choice in question.question_choices if choice.is_correct]
                # })
        if not is_correct:
            extraJson = {
                "error": True,
                "incorrect_choice": True,
                "message": "Wrong choice",
                "correct_choice": [choice.id for choice in question.question_choices if choice.is_correct]
            }
        
        mcq_completion = UserMCQCompletions()
        mcq_completion.question_id = question.id
        mcq_completion.user_id = current_user.id
        db.session.add(mcq_completion)
        db.session.commit()

    current_user_id = current_user.id
    question_mcq_completions = UserMCQCompletions.query.filter_by(user_id=current_user_id).all()
    all_questions = Question.query.order_by(Question.order).all()
    completed_question_ids = [completion.question_id for completion in question_mcq_completions]
    total_user_completed_questions = len(question_mcq_completions)
    total_questions = len(all_questions)
    for question in all_questions:
        if question.id in completed_question_ids:
            continue

        return jsonify({
            **question.to_response(), 
            **extraJson,
            "total_questions": total_questions,
            "total_completed_questions": total_user_completed_questions
        }), 200

    return jsonify({
        "is_finished": True, 
        "total_questions": total_questions,
        "total_completed_questions": total_user_completed_questions,
        **extraJson
    }), 200

@developer_bp.route("/mcqs", methods=["GET"])
@login_required
@module_enabled(MODULE_THEORY)
def list_mcqs():
    return render_template("mcq.html")

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

@developer_bp.route("/code_editor")
@login_required
def code_editor():
#    rdp_server = current_user.rdp_server_connection
    completed_challenges = UserCodeChallengeCompletions.query.filter_by(user_id=current_user.id).all()
    completed_challenge_ids = [completion.challenge_id for completion in completed_challenges]
    challenges = CodeChallenge.query.all()

    current_challenge = None
    for challenge in challenges:
        if challenge.id not in completed_challenge_ids:
            current_challenge = challenge
            break 

    current_challenge_id = current_challenge.id if current_challenge else None
    current_challenge_name = current_challenge.name if current_challenge else None

    return render_template("test.html", current_challenge=current_challenge, challenges=challenges, current_user=current_user)


@developer_bp.route("/code_editor/challenges", methods=["GET"])
@login_required
def list_codechallenges():
    all_challenges: list[CodeChallenge] = CodeChallenge.query.all()
    challenges_response = {
        "total": len(all_challenges),
        "challenges": [{
            "id": challenge.id,
            "name": challenge.name,
            "description": challenge.description,
            "vuln_code": challenge.vuln_code,
            "is_complete": (current_user in challenge.completed_users)
        } for challenge in all_challenges]
    }
    return jsonify(challenges_response)

@developer_bp.route("/code_editor/challenge/complete", methods=["POST"])
@login_required
def complete_codechallenge():
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

    challenge: Challenge = CodeChallenge.query.get(form.challenge_id.data)
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
    
    challenge_completion = UserCodeChallengeCompletions()
    challenge_completion.user_id = current_user.id
    challenge_completion.challenge_id = challenge.id

    db.session.add(challenge_completion)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Challenge completed successfully!"
    })

@developer_bp.route("/code_editor/current_challenge", methods=["GET"])
@login_required
def list_currentchallenges():
    completed_challenges = UserCodeChallengeCompletions.query.filter_by(user_id=current_user.id).all()
    completed_challenge_ids = [completion.challenge_id for completion in completed_challenges]
    challenges = CodeChallenge.query.all()

    current_challenge = None
    for challenge in challenges:
        if challenge.id not in completed_challenge_ids:
            current_challenge = challenge
            break 

    current_challenge_id = current_challenge.id if current_challenge else None
    current_challenge_name = current_challenge.name if current_challenge else None
    challenge_response = {
        "id": current_challenge_id,
        "name": current_challenge_name, 
    }
    return jsonify(challenge_response)

@developer_bp.route("/code_editor/submit_challenge", methods=["POST"])
@login_required
def submit_challenge():
    data = request.get_json()

    code = data.get("code")
    challenge_id = data.get("id")

    response = {
        "status": "success",
        "message": "Code received successfully",
        "completed": False
    }
    return jsonify(response)
