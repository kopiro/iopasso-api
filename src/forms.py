from wtforms import Form, StringField, PasswordField, DateField, DateTimeField, validators
from wtforms.fields.simple import HiddenField


class LoginForm(Form):
    email = StringField("email", validators=[
        validators.Length(min=7, max=100),
        validators.DataRequired(message="Email is required")
    ])
    password = PasswordField("password", validators=[
        validators.DataRequired(message="Password is required")
    ])


class RecoverForm(Form):
    email = StringField("email", validators=[
        validators.Length(min=7, max=100),
        validators.DataRequired(message="Email is required")
    ])


class ChangePasswordForm(Form):
    password = PasswordField("password", validators=[
        validators.DataRequired(message="Password is required"),
        validators.EqualTo(fieldname="password_2",
                           message="The password doesn't match")
    ])
    password_2 = PasswordField("password_2", validators=[
        validators.DataRequired(message="Confirm password is required")
    ])
    token = HiddenField("token", validators=[
        validators.DataRequired(message="Token is required")
    ])


class RegisterForm(Form):
    name = StringField("name", validators=[
        validators.Length(min=3, max=100),
        validators.DataRequired(message="Name is required")
    ])
    email = StringField("email", validators=[
        validators.Length(min=3, max=100),
        validators.DataRequired(message="Email is required")
    ])
    password = PasswordField("password", validators=[
        validators.DataRequired(message="Password is required"),
        validators.EqualTo(fieldname="password_2",
                           message="The password doesn't match")
    ])
    password_2 = PasswordField("password_2", validators=[
        validators.DataRequired(message="Confirm password is required")
    ])
    birth_date = DateField("birth_date", format="%Y-%m-%d")


class EventForm(Form):
    name = StringField("name", validators=[
        validators.Length(min=3, max=100),
        validators.DataRequired(message='Name is required')])
    address = StringField("address", validators=[
        validators.Length(min=3, max=100),
        validators.DataRequired(message='Address is required')])
    datetime = DateTimeField("datetime", format="%Y-%m-%dT%H:%M", validators=[
        validators.DataRequired(message='DateTime is required'),
    ])
    guests = StringField("guests", validators=[
        validators.DataRequired(message="Guests is required")
    ])
