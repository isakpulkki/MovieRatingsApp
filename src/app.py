from os import getenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv(
    "DATABASE_URL")
db = SQLAlchemy(app)

import routes
