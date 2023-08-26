from flask.views import MethodView
from src.db import *
from flask import render_template, request, redirect, session, flash
import bcrypt
import re


class login (MethodView):
    def get(self):
        return render_template('login.html')

    def post(self): 
        if request.method == 'POST' and 'nomeUsuario' in request.form and 'senhaUsuario' in request.form: 
            nomeUsuario = request.form['nomeUsuario'] 
            senhaUsuario = request.form['senhaUsuario'] 
            
            conexao = mysqlconector()
            cursor = conexao.cursor()
            
            cursor.execute('SELECT * FROM usuario WHERE nome_usuario = %s', (nomeUsuario, )) 
            account = cursor.fetchone()
            
            if account and bcrypt.checkpw(senhaUsuario.encode(), bytes(account[3])): 
                session['loggedin'] = True
                session['idUsuario'] = account[0]
                session['nomeUsuario'] = account[1]
                print(session['loggedin'])
                
                return redirect('/principal')
            else: 
                flash("Nome de usuario ou senha incorreto!")
            return redirect('/login')
        

class cadastrarUsuario (MethodView):
    def get(self):
        return render_template('cadastro.html')

    def post(self):
        if request.method == 'POST':
            nomeUsuario = request.form['nomeUsuario'] 
            emailUsuario = request.form['emailUsuario'] 
            senhaUsuario = request.form['senhaUsuario'] 
            confirmarSenha =  request.form['confirmarSenha']

            if nomeUsuario and emailUsuario and senhaUsuario:
                if senhaUsuario != confirmarSenha:
                    flash("Senhas não coincidem")
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailUsuario):
                    flash("Email inválido")
                elif not re.match(r'[A-Za-z0-9]+', nomeUsuario):
                    flash("O nome de usuário deve conter apenas caracteres e números!")
                else:
                    conexao = mysqlconector()
                    cursor = conexao.cursor()
                    cursor.execute('SELECT * FROM usuario WHERE nome_usuario = %s', (nomeUsuario,))
                    usuarios = cursor.fetchone()
                    if usuarios:
                        flash("Nome de usuário já existente")
                    else:
                        cursor.execute('SELECT * FROM usuario WHERE email_usuario = %s', (emailUsuario,))
                        usuarios = cursor.fetchone()
                        if usuarios:
                            flash("Email já existente")
                        else:
                            hashSenhaUsuario = bcrypt.hashpw(senhaUsuario.encode(), bcrypt.gensalt())
                            cursor.execute('INSERT INTO usuario VALUES (%s, %s, %s, %s)', (0, nomeUsuario, emailUsuario, hashSenhaUsuario))
                            conexao.commit()
                            cursor.close()
                            conexao.close()
                            flash("Cadastro realizado com sucesso")
            else:
                flash("Por favor, preencha o formulário!")

            return redirect('/cadastrar')

        return render_template('login.html')


class desconectarUsuario (MethodView):
    def get(self): 
        session.pop('loggedin', None) 
        session.pop('id', None) 
        session.pop('nome_usuario', None) 
        flash("sessao fechada")
        return redirect('/login')
        