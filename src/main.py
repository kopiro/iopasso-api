from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, StringField, PasswordField, validators
from flask_cors import CORS
import os

class LoginForm(Form):
    email = StringField("email", validators=[validators.Length(
        min=7, max=50), validators.DataRequired(message="Email is required")])
    password = PasswordField("password", validators=[
                             validators.DataRequired(message="Password is required")])

class RegisterForm(Form):
    name = StringField("first_name", validators=[validators.Length(
        min=3, max=25), validators.DataRequired(message="Name is required")])
    email = StringField("email", validators=[validators.Length(
        min=3, max=25), validators.DataRequired(message="Email is required")])
    password = PasswordField("password", validators=[
        validators.DataRequired(message="Password is required"),
        validators.EqualTo(fieldname="password2",
                           message="The password doesn't match")
    ])
    password2 = PasswordField("password2", validators=[
        validators.DataRequired(message="Confirm password is required")])
    birth_date = PasswordField("birth_date", validators=[
        validators.DataRequired(message="Birth date is required")])


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'usertable'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256), unique=True)


@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            birth_date=form.birth_date.data,
            password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True})
    else:
        return jsonify({'error':True,'validations':list(form.errors.items())})


if __name__ == '__main__':
    # Creating database tables
    db.create_all()
    # running server
    app.run(debug=True)
