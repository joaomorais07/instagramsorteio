from flask.views import MethodView
from src.db import *
from flask import render_template, request, redirect, url_for, session, flash
import re
from collections import OrderedDict
from playwright.sync_api import Playwright, sync_playwright
import time


class index (MethodView):
    def get(self):
        return render_template('index.html')
    

class principal (MethodView):
    def get(self):
        try:
            if session['loggedin'] == True:
                return render_template('principal.html')
            else:
                return redirect('/login')
        except:
            return redirect('/login')

        
class buscarComentatios (MethodView):
    def post(self):
        link =  request.form['link']

        with sync_playwright() as p:
            navegador = p.chromium.launch(headless=False)
            context = navegador.new_context(storage_state="state.json")
            pagina = context.new_page()
            pagina.goto(link, timeout=0)

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

        print(listaMaeFinal)