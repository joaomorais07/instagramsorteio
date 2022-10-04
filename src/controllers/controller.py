from flask.views import MethodView
from src.db import *
from flask import render_template, request, redirect, url_for, session, flash
import re

from collections import OrderedDict
from playwright.sync_api import Playwright, sync_playwright
from alive_progress import alive_bar
import keyboard
import colorama
import time
import random

class index (MethodView):
    def get(self):
        return render_template('index.html')

class login (MethodView):
    def get(self):
        return render_template('login.html')

    def post(self): 
        if request.method == 'POST' and 'nome_usuario' in request.form and 'senha' in request.form: 
            nome_usuario = request.form['nome_usuario'] 
            senha = request.form['senha'] 
            conexao = mysqlconector()
            cursor = conexao.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE nome_usuario = %s AND senha = %s', (nome_usuario, senha)) 
            account = cursor.fetchone()
            if account: 
                session['loggedin'] = True
                session['id'] = account[0]
                session['nome_usuario'] = account[1]
                print(session['loggedin'])
                return redirect('/principal')
                #flash('Login efetuado com sucesso!')
            else: 
                flash("Nome de usuario ou senha incorreto!")
            return redirect('/login')

class principal (MethodView):
    def get(self):
        try:
            if session['loggedin'] == True:
                return render_template('principal.html')
            else:
                return redirect('/login')
        except:
            return redirect('/login')

class desconectar (MethodView):
    def get(self): 
        session.pop('loggedin', None) 
        session.pop('id', None) 
        session.pop('nome_usuario', None) 
        flash("sessao fechada")
        return redirect('/login')

class cadastro (MethodView):
    def get(self):
        return render_template('cadastro.html')

    def post(self): 
        if request.method == 'POST' and 'nome_usuario' in request.form and 'email' in request.form and 'senha' in request.form : 
            nome_usuario = request.form['nome_usuario'] 
            email = request.form['email'] 
            senha = request.form['senha'] 
            confirmarSenha =  request.form['confirmarSenha']
            conexao = mysqlconector()
            cursor = conexao.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE nome_usuario = %s', (nome_usuario,)) 
            usuarios = cursor.fetchone()
            if usuarios: 
                flash("Nome de usuario ja existente")
                return redirect('/cadastro')
            cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,)) 
            usuarios = cursor.fetchone()
            if usuarios:
                flash("Email ja existente2")
                return redirect('/cadastro')
            elif senha != confirmarSenha:
                flash("Senhas não coencidem")
                return redirect('/cadastro')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
                flash("Email invalido")
                return redirect('/cadastro')
            elif not re.match(r'[A-Za-z0-9]+', nome_usuario): 
                flash("O nome de usuário deve conter apenas caracteres e números!")
                return redirect('/cadastro')
            elif not nome_usuario or not senha or not email: 
                flash("Por favor, preencha o formulário !")
                return redirect('/cadastro')
            else: 
                cursor.execute('INSERT INTO usuarios VALUES (%s, %s, %s, %s)', (0, nome_usuario, email, senha)) 
                conexao.commit()
                cursor.close()
                conexao.close()
                flash("Cadastro realizado com sucesso")
        elif request.method == 'POST': 
            flash('Por favor, preencha o formulário!')
            return redirect('/cadastro')
        return render_template('login.html')

        
class teste (MethodView):
    def run(playwright: Playwright) -> None:
        global listaComentarios, listaNomes, listaRespostas
        navegador = playwright.chromium.launch(headless=False)
        context = navegador.new_context(storage_state="state.json")
        pagina = context.new_page()
        pagina.goto("https://www.instagram.com/p/Ch-Z6o-vRwI/", timeout=0)

        trava = 0
        while trava == 0:
            time.sleep(0.6)
            listaNomes = pagina.locator('._a9zc').all_text_contents()
            listaComentarios = pagina.locator('._a9zs').all_text_contents()
            try:
                pagina.locator("[aria-label='Carregar mais comentários']").dispatch_event('click', timeout=10000)
            except:
                if len(listaComentarios) > 1300:
                    trava += 1
                else:
                    listaNomes.clear()
                    listaComentarios.clear()
                    pagina.reload()
                if len(listaComentarios) != len(listaNomes):
                    trava = 0

        time.sleep(2)
        context.close()
        navegador.close()
        print("pronto")


    with sync_playwright() as playwright:
        run(playwright)

    print(listaNomes)
    print(listaComentarios)

    vermelho = colorama.Fore.LIGHTRED_EX
    branco = colorama.Fore.LIGHTWHITE_EX
    print(vermelho+"$$$$SORTEIO OFICIAL DO SITE MEU MONEY$$$$")
    print(branco+"pressione f4 para iniciar")

    trava = 0
    while trava == 0:
        if keyboard.read_key() == "f4":
            azul = colorama.Fore.LIGHTBLUE_EX
            print(azul+"BUSCANDO TODOS OS COMENTÁRIOS")
            with alive_bar(
                    len(listaNomes),
                    title=f"{azul}aguarde",
                    unknown="waves",
                    force_tty=True,
                    dual_line=True,
            )as bar:
                for i in listaNomes:
                    time.sleep(0.02)
                    bar()
            trava += 1
            print("PRONTO")
            print()

    listaNomesValidos = []
    listaComentariosValidos = []
    busca = "@"
    i = 0
    for s in listaComentarios:
        if busca in s:
            listaComentariosValidos.append(s)
            listaNomesValidos.append(listaNomes[i])
            i += 1
        else:
            i += 1

    listaMae = []
    for nome, comentario in zip(listaNomesValidos, listaComentariosValidos):
        listaMae.append((nome, comentario))

    listaMaeFinal = list(OrderedDict.fromkeys(listaMae))

    amarelo = colorama.Fore.LIGHTYELLOW_EX
    verde = colorama.Fore.LIGHTGREEN_EX
    magenta = colorama.Fore.LIGHTMAGENTA_EX
    print(branco+f"TIVEMOS O TOTAL DE: {amarelo}{len(listaMaeFinal)} COMENTÁRIOS VALÍDOS")
    print()

    print(magenta+"##PRESSIONE F4 PARA SORTEAR##")
    while True:
        if keyboard.read_key() == "f4":
            with alive_bar(
                    100,
                    title=f"{magenta} SORTEANDO O NOSSO GANHADOR....",
                    force_tty=True,
            ) as bar:
                for i in range(100):
                    time.sleep(0.05)
                    bar()
            n = random.randint(0, len(listaMaeFinal)-1)
            print()
            print(f"{branco}O VENCEDOR DO NOSSO SORTEIO FOI: {verde}{listaMaeFinal[n][0].upper()}")
            print(f"{branco}COM O COMENTÁRIO: {amarelo}{listaMaeFinal[n][1]}")
            print(f"{branco}POSIÇÃO: {amarelo}{n}")
            time.sleep(2)
            print()
            print(magenta + "##PRESSIONE F4 PARA SORTEAR NOVAMENTE##")