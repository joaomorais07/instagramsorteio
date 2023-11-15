from flask import Flask
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

from src.routes.routes import *

app.config['SECRET_KEY'] = "senha"
