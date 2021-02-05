from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import Flask
from os import getcwd, getenv
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)

db_filename = 'sqlite:///' + getcwd() + '/data/db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = getenv('SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)
CORS(app)
