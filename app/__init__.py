from flask import Flask
from flask_jwt_extended import  JWTManager
from flasgger import Swagger
from flask_cors import CORS
from os import environ
import config
#from app import app

env = environ.get("APP_SETTINGS")
app = Flask(__name__)
CORS(app,supports_credentials=True)
app.config.from_object(env)
print(env)

app.config['JWT_SECRET_KEY'] = "secret"
jwt = JWTManager(app)
swag = Swagger(app)
from app.views import auth_views,order_views,menu_views




