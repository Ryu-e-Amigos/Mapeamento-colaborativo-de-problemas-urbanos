# Abre o 'requirements.txt'

from flask import Flask, render_template, redirect, request, flash, url_for, session
import json
import pyperclip
import pandas as pds
import folium
import folium.plugins
import geopandas as gpds
from BancoDeDados import enderecoDao, reportDao, usuarioDao
from BancoDeDados.connection import mostrandoReports

#iniciando
app = Flask(__name__)
app.config['SECRET_KEY'] = "batatamuitofrita"

#rotas
@app.route('/', methods = ["POST", "GET"])
def login():
    return render_template("login.html")

@app.route('/mapa.html')
def main():
    return render_template("mapa.html")

@app.route('/cadastro.html')
def cadastro():
    return render_template("cadastro.html") 

@app.route('/report.html')
def report():
    return render_template("report.html")

@app.route('/report', methods = ["POST"])
def verificaLogin():
    usuario_login = request.form.get("usuario")
    senha_login = request.form.get("senha")
    newUsuarioDao = usuarioDao.Usuario()
    login = newUsuarioDao.verificaLogin(usuario_login, senha_login)

    if login:
        print(login[0])
        session['usuario_id'] = login[0]  # Armazena o ID do usuário na sessão
        return redirect(url_for("report"))
    else:
        flash("Usuário Inválido")
        return redirect(url_for("login"))
            
@app.route('/cadastro', methods = ["POST"])
def criaConta():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    confSenha = request.form.get("confSenha")
    if senha == confSenha:
        newUsuarioDao = usuarioDao.Usuario()
        newUsuarioDao.salvarNovo(usuario, senha)
        return redirect(url_for("report"))
    else:
        flash("Senha e confirmação diferentes!")
        return redirect(url_for("cadastro"))

@app.route('/toMap', methods = ["POST"])
def mapa():
    print(session['usuario_id'])
    if 'usuario_id' not in session:
        print('Você precisa estar logado para salvar um report.')
        flash("Você precisa estar logado para salvar um report.")
        return redirect(url_for("login"))
    else:
        print('Usuario logado.')

    #Pegando a localização - EX: R. Manoel Santos Chieira, 92
    cidade = request.form.get("cidade")
    print(cidade)
    rua = request.form.get("rua")
    print(rua)
    nmr = request.form.get("nmr")
    print(nmr)
    comp = request.form.get("comp")
    print(comp)
    end =  [rua, nmr, cidade]
    corPin = request.form["situacao"]
    print(corPin)
    # coord = gpds.tools.geocode(end, provider = "nominatim", user_agent = "myGeocode")["geometry"]  # só funciona na janela interativa
    # string = str(coord[0])
    # separacao = string.split()
    # separacao.remove(separacao[0])
    # lat = (separacao[1].replace(')',''))
    # lon = (separacao[0].replace('(',''))
    
    newEnderecoDao = enderecoDao.endereco()
    newEnderecoId = newEnderecoDao.salvarNovo(rua, cidade, nmr, comp)
    newReportDao = reportDao.Report()
    newReportDao.salvarNovo(corPin, newEnderecoId, session['usuario_id']) # Pega o ID do usuário da sessão



    #Configurações do mapa
    m = folium.Map(location=(-22.2127829,-49.9557924), zoom_start = 12, control_scale = False, )
    folium.plugins.Geocoder().add_to(m)
    folium.plugins.Fullscreen(position="topright", title="Expand me", title_cancel="Exit me", force_separate_button=True).add_to(m)




#   ======================================    INVERSÃO DE FLUXO    ==========================================


    # Marcador
    puxarReports(m)

    # Legenda
    legend_html = '''
     <div style="position: fixed; 
     bottom: 5px; left: 5px; width: 200px; height: 200px; 
     border: 2px solid grey; z-index: 9999; font-size: 18px;
     background-color: white; text-align: center; padding: 10px;
     border-radius: 6px;
     ">&nbsp; <b style="font-size: 22px">Legenda</b> <br>
     &nbsp; Buraco &nbsp; <i class="fa fa-map-marker fa-2x" style="color:#d53e2a"></i><br>
     &nbsp; Semáforo &nbsp; <i class="fa fa-map-marker fa-2x" style="color:#36a3d3"></i><br>
     &nbsp; Vazamento &nbsp; <i class="fa fa-map-marker fa-2x" style="color:#6eaa25"></i><br>
     &nbsp; Obstrução &nbsp; <i class="fa fa-map-marker fa-2x" style="color:#2e2e2e"></i><br>
      </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    botao_html = '''
     <button style="position: fixed; ">Confirmar</button>
     '''
    m.get_root().html.add_child(folium.Element(botao_html))
    
    # Rodando
    m.save("templates/mapa.html")
    return redirect(url_for("main"))

#Função do Banco
def puxarReports(m):
    df = mostrandoReports()

    rua_lista = df['rua'].tolist()
    cidade_lista = df['cidade'].tolist()
    numero_lista = df['numero'].tolist()
    situacao_lista = df['situacao'].tolist()

    for i in range(0, len(df), 1):
        end = [rua_lista[i], numero_lista[i], cidade_lista[i]]

        coord = gpds.tools.geocode(end, provider="nominatim", user_agent="myGeocode")["geometry"]
        string = str(coord[0])
        separacao = string.split()
        separacao.remove(separacao[0])
        lat = (separacao[1].replace(')',''))
        lon = (separacao[0].replace('(',''))

        corPin = situacao_lista[i]
        if corPin == 1:
            folium.Marker(location=[lat, lon], icon=folium.Icon(color='red')).add_to(m)
        elif corPin == 2:
            folium.Marker(location=[lat, lon], icon=folium.Icon(color='blue')).add_to(m)
        elif corPin == 3:
            folium.Marker(location=[lat, lon], icon=folium.Icon(color='green')).add_to(m)
        else:
            folium.Marker(location=[lat, lon], icon=folium.Icon(color='black')).add_to(m)

#execução
if __name__ == "__main__":
    app.run(debug = True)