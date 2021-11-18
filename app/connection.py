from sqlalchemy.sql import text

from app import app
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()
import os
DATABASE_URI = os.getenv('DB_TYPE') + os.getenv("DB_USERNAME") + os.getenv("DB_PASSWORD") + os.getenv("DB_HOST") + os.getenv("DB_NAME")

app.secret_key = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
