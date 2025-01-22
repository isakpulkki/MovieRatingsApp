from os import getenv
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask
load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv(
    "DATABASE_URL")
db = SQLAlchemy(app)

import routes