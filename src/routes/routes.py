from src.controllers.controller import *



routes={
    "index_route":"/","index_controller":index.as_view("index"),
    "cadastro_route":"/cadastro","cadastro_controller":cadastro.as_view("cadastro"),
    "login_route":"/login","login_controller":login.as_view("login"),
    "principal_route":"/principal","principal_controller":principal.as_view("principal"),
    
}

