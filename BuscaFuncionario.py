# encoding: utf-8
from flask import  Flask, request, jsonify
import os
import time
import json
import sqlite3
import hmac
import hashlib
import base64


def BuscaFuncionario(jsonclient):
  token = jsonclient["token"]
  
  secret_key = '52d3f853c19f8b63c0918c126422aa2d99b1aef33ec63d41dea4fadf19406e54'
  JWT = token
  
  b64_header, b64_payload, b64_signature = JWT.split('.')
  b64_signature_checker = base64.urlsafe_b64encode(
      hmac.new(
          key=secret_key.encode(), 
          msg=f'{b64_header}.{b64_payload}'.encode(), 
          digestmod=hashlib.sha256
      ).digest()
  ).decode()
  
  payload = json.loads(base64.urlsafe_b64decode(b64_payload))
 
  if b64_signature_checker != b64_signature:
      raise Exception('Assinatura inválida')
  
  
  cpf3 = str("cpf"+jsonclient["cpf"])
  data = jsonclient["data"]
  data = data.replace("/","")
  
  if len(data) == 6:
  	query = f"SELECT * FROM {cpf3} WHERE Data LIKE '__{data}'"
  	
  	
  elif len(data) == 8:
  	query = f"SELECT * FROM {cpf3} WHERE Data LIKE '{data}'"
  else:
  	resp = {"error": "error"}
  	return resp
  	
  #conexao com banco dados
  conecxao = sqlite3.connect('usuarios.db')
  cursor = conecxao.cursor()
  print("Conectado ao banco de dados")
  
  try:
  	cursor.execute(query)

  	verifica_entrada = cursor.fetchall()
  	
  	print('sou verifa',verifica_entrada)
  	
  	if verifica_entrada:
  		lista_posto = verifica_entrada
  		
  		resp = {"status": lista_posto}
  		return resp

  	elif verifica_entrada == []:
  		resp = {"erro": "Usuário não tem nenhum dado!!"}
  		return resp
			
  
  except sqlite3.Error as error:
  	print("Falha ao excluir posto", error)
  	resp = {"error": "error"}
  	return resp
	


