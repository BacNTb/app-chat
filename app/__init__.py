from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
import random, string

app = Flask(__name__)
CORS(app, support_credentials=True)

app.config["JWT_SECRET_KEY"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)

jwt = JWTManager(app)

from app import route
