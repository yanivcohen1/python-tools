from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS, cross_origin

from flask_restful import Api
from database.db import initialize_db
from resources.errors import errors

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION') # read from config file
print("SECRET_KEY:" + app.config["JWT_SECRET_KEY"]) # read from config file a key
print("config read all keys:")
print(app.config) # read from config file all keys
mail = Mail(app)

api = Api(app, errors=errors)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)

# imports requiring app and mail
from resources.routes import initialize_routes
initialize_routes(api)
