# encoding: utf-8
from flask import  Flask, request, jsonify
import os
import time
import json
import sqlite3
import hmac
import hashlib
import base64

#rota principal envia dados json 
def CadastroAdm(jsonclient):
  
  nome = jsonclient["nome"]
  cpf = jsonclient["cpf"]
  fone = jsonclient["fone"]
  email = jsonclient["email"]
  senha = jsonclient["senha"]
  token = "123456"
  cpf = cpf.replace(".", "")
  cpf = cpf.replace("-", "")
  cpf2 = str("cpf"+cpf)
  cpf3 = str("extra"+cpf)
  cpf4 = str("posto"+cpf)
  print(cpf)
  #cria conexão ao banco
  conecxao = sqlite3.connect('usuarios.db')
  cursor = conecxao.cursor()
  print("Conectado ao banco de dados")
  
  #faz busca a usuário no banco 
  cursor.execute(f"SELECT * FROM encarregados WHERE Cpf={cpf}")
 
 
  verifica_entrada = cursor.fetchone()
  
  print("souuu",verifica_entrada)
  
  if verifica_entrada == None:
    print("Cadastrando usuario")
    cursor.execute("""INSERT INTO encarregados(Nome, Cpf, Fone, Token, Email, Senha) VALUES(?, ?, ?, ?, ?,?)""", (nome,cpf, fone, token, email, senha))
    conecxao.commit()

    
                           
    print("usuario criado com sucesso")
    
    secret_key = '52d3f853c19f8b63c0918c126422aa2d99b1aef33ec63d41dea4fadf19406e54'
    
    header = json.dumps({
        'typ': 'JWT',
        'alg': 'HS256'
    }).encode()
    
    payload = json.dumps({
        'senha': senha,
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
    
    print("final",JWT)
    return {"token": JWT}
    
  else:
    return {"status":"erro"}
   