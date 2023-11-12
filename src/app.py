from flask import Flask

app = Flask(__name__)

from src.routes.routes import *

app.config['SECRET_KEY'] = "senha"
