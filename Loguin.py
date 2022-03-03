# encoding: utf-8
from flask import  Flask, request, jsonify
import os
import time
import json
import sqlite3
import hmac
import hashlib
import base64



def Loguin(jsonclient):
  senha = jsonclient["senha"]
  
  cpf = jsonclient["cpf"]
 
  print("uuiii",jsonclient)
  #cria conexão ao banco
  conecxao = sqlite3.connect('usuarios.db')
  cursor = conecxao.cursor()
  print("Conectado ao banco de dados")
  print(type(cpf))
  try:
    #faz busca a usuário no banco 
    cursor.execute(f"SELECT * FROM funcionarios WHERE Cpf={cpf} and Senha={senha}")
   
    verifica_entrada = cursor.fetchone()
    print("$$$",verifica_entrada)
    confcpf = verifica_entrada[2]
    confsenha = verifica_entrada[6]
    print(confcpf,confsenha,"&&",cpf,senha)
    
    if confcpf == cpf and confsenha == senha:
      
      
      secret_key = '52d3f853c19f8b63c0918c126422aa2d99b1aef33ec63d41dea4fadf19406e54'
      
      header = json.dumps({
          'typ': 'JWT',
          'alg': 'HS256'
      }).encode()
      
      payload = json.dumps({
          'cpf': cpf,
      }).encode()
      
      b64_header = base64.urlsafe_b64encode(header).decode()
      b64_payload = base64.urlsafe_b64encode(payload).decode()
      
      signature = hmac.new(
          key=secret_key.encode(), 
          msg=f'{b64_header}.{b64_payload}'.encode(),
          digestmod=hashlib.sha256
      ).digest()
      
      JWT = f'{b64_header}.{b64_payload}.{base64.urlsafe_b64encode(signature).decode()}'
      
      print(JWT)
      resp = {"token": JWT}
      return resp
     
       
  except:
    resp = {"status":"erro"}
    print("Erro!!")
    return resp
    
 