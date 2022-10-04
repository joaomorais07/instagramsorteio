from flask import Flask
from src.routes.routes import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "senha"

app.add_url_rule(routes["index_route"],view_func=routes["index_controller"])
app.add_url_rule(routes["cadastro_route"],view_func=routes["cadastro_controller"])
app.add_url_rule(routes["desconectar_route"],view_func=routes["desconectar_controller"])
app.add_url_rule(routes["login_route"],view_func=routes["login_controller"])
app.add_url_rule(routes["principal_route"],view_func=routes["principal_controller"])

