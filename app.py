from flask import  Flask, request, jsonify
import os
import time
import json
import sqlite3
import hmac
import hashlib
import base64

from EntradaManual import EntradaManual
from CadastroUser import CadastroUser
from Loguin import Loguin
from BuscaPostos import BuscaPostos
from ExcluirPosto import ExcluirPosto
from CadastraPosto import CadastraPosto
from HoraExtra import HoraExtra
from Horarios import Horarios
from CadastroFechamento import CadastroFechamento

app = Flask(__name__)

#endpoint para encarregado de cadastrar entradas de funcionarios   
@app.route("/entradamanual", methods=["POST"])
def entradamanual():
  print("rota postos")
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)

  retorno = EntradaManual(jsonclient)
  resp = jsonify(retorno)

  resp.headers['Access-Control-Allow-Origin']='*'
  return resp


@app.route("/busca_postos", methods=["POST"])

def busca_postos():

  print("busca postos")
  #bodyss = request.get_json()
  #body= request.form.get('language')
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)
  print(jsonclient)
  
  retorno = BuscaPostos(jsonclient)
  resp = jsonify(retorno)

  resp.headers['Access-Control-Allow-Origin']='*'
  return resp

@app.route("/excluir_postos", methods=["POST"])
def excluir_postos():

  print("excluí postos")
 
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)
  print(jsonclient)

  retorno = ExcluirPosto(jsonclient)
  resp = jsonify(retorno)

  resp.headers['Access-Control-Allow-Origin']='*'
  return resp
  


@app.route("/cadastra_postos", methods=["POST"])
def postos():
  print("rota postos")
  #bodyss = request.get_json()
  #body= request.form.get('language')
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)
  print(jsonclient)
  
  retorno = CadastraPosto(jsonclient)
  resp = jsonify(retorno)

  resp.headers['Access-Control-Allow-Origin']='*'
  return resp
  
  
@app.route("/cadastrofechamento", methods=["POST"])
def cadastrofechamento():

  print("cadasto fechamento")
  #bodyss = request.get_json()
  #body= request.form.get('language')
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)
  
  print(jsonclient)

  retorno = CadastroFechamento(jsonclient)
  
  resp = jsonify(retorno)
  resp.headers['Access-Control-Allow-Origin']='*'
  return resp
  


#rota de cadastro dos funcionarios 
@app.route("/cadastro", methods=["POST"])
def loguin():
  print("cadasto")
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)
  JWT = CadastroUser(jsonclient)
  
  resp = jsonify(JWT)
  resp.headers['Access-Control-Allow-Origin']='*'
  return resp
  

#end point de loguin de usuarios
@app.route("/loguin", methods=["POST"])
def loguins():
  print("requestloguin")
  
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)
  
  retorno = Loguin(jsonclient)
  
  resp = jsonify(retorno)
  resp.headers['Access-Control-Allow-Origin']='*'
  return resp
  
  
@app.route("/horarios", methods=["POST"])
def horarios():
  print("horários")
  #bodyss = request.get_json()
  #body= request.form.get('language')
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)
  print(jsonclient)
  
  retorno = Horarios(jsonclient)
  resp = jsonify(retorno)

  resp.headers['Access-Control-Allow-Origin']='*'
  return resp


  
@app.route("/horaextra", methods=["POST"])

def horaextra():

  print("horários")
  #bodyss = request.get_json()
  #body= request.form.get('language')
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)
  print(jsonclient)

  retorno = HoraExtra(jsonclient)
  resp = jsonify(retorno)

  resp.headers['Access-Control-Allow-Origin']='*'
  return resp


  
if  __name__ == "__main__":

    HOST = os.environ.get('SERVER_HOST', '127.0.0.1')
    try:
        PORT = int(os.environ.get('SERVER_PORT', "5000"))

    except ValueError:
        PORT = 5000
    
    #inicia aplicaçao
    app.run(HOST,PORT)
    #webview.start(HOST, PORT)


