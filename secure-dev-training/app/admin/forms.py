from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
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