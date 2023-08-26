from src.controllers.controller import *
from src.controllers.usuario_controller import *
from src.controllers.rotas_controller import *


app.add_url_rule('/cadastrar', view_func=cadastrarUsuario.as_view('cadastrar')),
app.add_url_rule('/desconectar',view_func=desconectarUsuario.as_view('desconectar')),
app.add_url_rule('/login', view_func=login.as_view("login")),
app.add_url_rule('/principal', view_func=principal.as_view("principal"))
app.add_url_rule('/', view_func=index.as_view('index'))
app.add_url_rule('/listarRotas', view_func=listarRotas.as_view('listar_rotas'))

