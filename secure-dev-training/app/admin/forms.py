from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, FieldList, FormField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")

class AddRDPServersForm(FlaskForm):
    rdp_servers = StringField("RDP Servers", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit RDP servers")

class ChangeLoginCodeForm(FlaskForm):
    class Meta:
        csrf = False

    login_code = StringField("Login code")

class DeleteUserForm(FlaskForm):
    class Meta:
        csrf = False

    user_id = IntegerField("User ID", validators=[DataRequired()])


class MCQChoice(FlaskForm):
    class Meta:
        csrf = False
        
    choice_text = StringField("Choice text", validators=[DataRequired()])
    is_correct = BooleanField("Is Correct")

class MCQForm(FlaskForm):
    class Meta:
        csrf = False
        
    question_text = StringField("Question text", validators=[DataRequired()])
    choices = FieldList(FormField(MCQChoice), min_entries=4)
    submit = SubmitField("Submit")


class MCQOrder(FlaskForm):
    class Meta:
        csrf = False

    mcq = IntegerField("mcq", validators=[DataRequired()])
    order = IntegerField("order", validators=[DataRequired()])

class ReorderMCQForm(FlaskForm):
    class Meta:
        csrf = False

    reordering = FieldList(FormField(MCQOrder), min_entries=1)