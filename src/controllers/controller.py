from flask.views import MethodView
from src.db import *
from flask import render_template, request, redirect, url_for, session, flash
import re

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
                session['logado'] = True
                #session['id'] = account['id'] 
                #session['nome_usuario'] = account['nome_usuario'] 
                #flash('Login efetuado com sucesso!')
                return redirect('/principal') 
            else: 
                flash("Nome de usuario ou senha incorreto!")
            return redirect('/login')
  
'''@app.route('/desconetar') 
def desconectar(): 
    session.pop('logado', None) 
    session.pop('id', None) 
    session.pop('nome_usuario', None) 
    return redirect(url_for('login'))'''

class cadastro (MethodView):
    def get(self):
        return render_template('cadastro.html')

    def post(self): 
        if request.method == 'POST' and 'nome_usuario' in request.form and 'email' in request.form and 'senha' in request.form : 
            nome_usuario = request.form['nome_usuario'] 
            email = request.form['email'] 
            senha = request.form['senha'] 
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
        return render_template('cadastro.html')


class principal (MethodView):
    def get(self):
        return render_template('principal.html')
