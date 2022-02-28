from flask import  Flask, request, jsonify
import os
import time
import json
import sqlite3
import hmac
import hashlib
import base64

def ExcluirPosto(jsonclient):
    
  token = jsonclient["token"]
  id_posto = jsonclient["id"]
 
  print("@@@@@",token)
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
  
  print("&&&&&&&&",payload["cpf"])
  
  cpf3 = str("posto"+payload["cpf"])
  
  #conexao com banco dados
  conecxao = sqlite3.connect('usuarios.db')
  cursor = conecxao.cursor()
  print("Conectado ao banco de dados excluir posto")
  
  cursor.execute(f"SELECT * FROM {cpf3} WHERE ID={id_posto}")
  
  verifica_posto = cursor.fetchall()
  
  print('sou verifa postooo',verifica_posto)
  lista_posto = verifica_posto
  
  print(lista_posto)
  
  if lista_posto !=[]:
    try:
        sql_delete_query = f"DELETE FROM {cpf3} WHERE ID={id_posto}"
        
        cursor.execute(sql_delete_query)
        conecxao.commit()
        
        
        print("Posto deletado",sql_delete_query)
        cursor.close()
        
        resp = {"status": "Posto excluído com sucesso!!"}
          
        return resp
        

    except sqlite3.Error as error:
        print("Falha ao excluir posto", error)
        
        resp = {"status": "Erro ao excluir posto!!"}

        return resp

    finally:
        if conecxao:
            conecxao.close()
            print("banco de dados fechado")
  
  else:
    resp = {"status": "Posto inexistente!!"}
  
    return resp
   