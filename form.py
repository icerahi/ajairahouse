from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email

class RegistrationForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=2)])
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])

    submit=SubmitField("Register")

class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    remember=BooleanField("remember me")
    submit=SubmitField("Login")
