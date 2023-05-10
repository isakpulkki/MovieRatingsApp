from os import getenv
from flask import Flask
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv(
    "DATABASE_URL").replace("://", "ql://", 1)

import routes
import users
