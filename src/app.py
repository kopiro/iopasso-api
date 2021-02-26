from flask import jsonify
from models import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask import Flask
from os import getcwd, getenv
from flask_migrate import Migrate
import routes.events
import routes.users
import routes.guests
import routes.auth
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + getcwd() + \
    '/data/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SALT_KEY'] = getenv('SALT_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['SERVER_NAME'] = getenv('SERVER_NAME')

db.init_app(app)
Migrate(app, db)

jwt = JWTManager(app)
CORS(app)

app.register_blueprint(routes.auth.blue, url_prefix='/auth')
app.register_blueprint(routes.events.blue, url_prefix='/events')
app.register_blueprint(routes.guests.blue, url_prefix='/guests')
app.register_blueprint(routes.users.blue, url_prefix='/users')


@app.errorhandler(Exception)
def handle_bad_request(ex):
    return jsonify({
        'error': True,
        'message': str(ex)
    }), 500


@app.before_first_request
def before_first_request():
    db.create_all()


if __name__ == "__main__":
    app.run()
