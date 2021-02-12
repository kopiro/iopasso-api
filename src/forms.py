from wtforms import Form, StringField, PasswordField, DateField, DateTimeField, validators
from wtforms.fields.core import SelectMultipleField


class LoginForm(Form):
    email = StringField("email", validators=[
        validators.Length(min=7, max=100),
        validators.DataRequired(message="Email is required")
    ])
    password = PasswordField("password", validators=[
        validators.DataRequired(message="Password is required")
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
    birth_date = PasswordField("birth_date")


class EventForm(Form):
    name = StringField("name", validators=[
        validators.Length(min=3, max=100),
        validators.DataRequired(message='Name is required')])
    address = StringField("address", validators=[
        validators.Length(min=3, max=100),
        validators.DataRequired(message='Address is required')])
    # WARNING: the space after the format is mandatory!!
    datetime = DateTimeField("datetime", format="%Y-%m-%dT%H:%M ", validators=[
        validators.DataRequired(message='DateTime is required'),
    ])
    guests = StringField("guests", validators=[
        validators.DataRequired(message="Guests is required")
    ])
