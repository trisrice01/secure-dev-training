from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in...")

class AddRDPServersForm(FlaskForm):
    rdp_servers = StringField("RDP Servers", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit RDP servers")