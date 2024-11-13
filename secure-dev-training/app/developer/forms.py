from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FieldList
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Re-Enter password", validators=[DataRequired()])
    login_code = StringField("Login Code", validators=[DataRequired()])
    submit = SubmitField("Sign in")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")


class CompleteMCQForm(FlaskForm):
    class Meta:
        csrf = False

    question_id = IntegerField("Question ID", validators=[DataRequired()])
    choice_ids = FieldList(IntegerField(), min_entries=1)


class ChallengeCompletionForm(FlaskForm):
    class Meta:
        csrf = False
        
    challenge_id = IntegerField("Challenge ID", validators=[DataRequired()])
    challenge_flag = StringField("Challenge Flag", validators=[DataRequired()])

