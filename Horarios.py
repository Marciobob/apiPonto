from flask import  Flask, request, jsonify
import os
import time
import json
import sqlite3
import hmac
import hashlib
import base64


def Horarios(jsonclient):
    
  token = jsonclient["token"]
  botao = jsonclient["botao"]
  endereco = jsonclient["endereco"]
  numero = jsonclient["numero"]
  hora = jsonclient["hora"]
  data = jsonclient["data"]
  
  data = data.replace("/","")
  
  horas = hora.replace(":","")
  
  print(token,endereco,numero,data,hora,botao)
  
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
  
  print("&&&&&&&&",payload["cpf"],horas)
  
  cpf3 = str("cpf"+payload["cpf"])
  
  cpf_posto = str("posto"+payload["cpf"])
  #conexao com banco dados
  conecxao = sqlite3.connect('usuarios.db')
  cursor = conecxao.cursor()
  print("Conectado ao banco de dados")
  
  #confere se o endereço de entrada esta igual ao cafastrado no posto
  cursor.execute(f"SELECT * FROM {cpf_posto}")
  query_posto = cursor.fetchall()
  print("confere endereço",query_posto)
  
  if query_posto == []:
    resp = {"status":"Você não tem bnenhum posto cadastrado!!"}
    return resp
  
  elif query_posto[0][2] == endereco:
    print("conferido endereçoooooo")
   
    cursor.execute(f"SELECT * FROM {cpf3}")
    verifica_entrada = cursor.fetchall()
    
    print('sou verifa',verifica_entrada)
    
    if botao == "Entrada":
      for result in verifica_entrada:
        print(result)
        dia = result[1]
        horario = result[2]
        print(dia,horario,"$$$$$$$$$$$",data,horas)
        
        if dia == data and horario != None:
          resp = {"status":"erro"}
        
          return resp
    
      print("Entrada")
      cursor.execute("""INSERT INTO {}(Data,Entrada,Endereco,Numero) VALUES(?, ?, ?, ?)""".format(cpf3), (data,horas,endereco,numero))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      print('sou verifica',verifica_entradas)
      
      resp = {"status":"Entrada efetuada com sucesso!!"}      
      return resp
    

    elif botao == "Almoço":
      print("saindo para almoçar")
      for result in verifica_entrada:
            print(result)
            dia = result[1]
            horario = result[4]
            print(dia,horario,"$$$$$$$$$$$",data,horas)
            
            if dia == data and horario != None:
              resp = {"status":"erro"}
            
              return resp


      print("Saindo para o almoço")
      cursor.execute("""UPDATE {} SET Almoco_entra=? WHERE Data=?""".format(cpf3),(horas,data))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      print('sou verificassss',verifica_entradas)

      resp = {"status":"Saida para o almoço efetuada com sucesso!!"}   
      return resp
    

    elif botao == "Retorno almoço":
      print("saindo para almoçar")
      for result in verifica_entrada:
        print(result)
        dia = result[1]
        horario = result[5]
        print(dia,horario,"$$$$$$$$$$$",data,horas)
            
        if dia == data and horario != None:
          resp = {"status":"erro"}          
          return resp
  
      print("Entrada")
      cursor.execute("""UPDATE {} SET Almoco_saida=? WHERE Data=?""".format(cpf3),(horas,data))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      
      print('sou verificassss',verifica_entradas)
      
      resp = {"status":"Retorno do almoço efetuado com sucesso!!"}      
      return resp
    

    elif botao == "Café":
      print("cafe",botao)
      for result in verifica_entrada:
        print(result)
        dia = result[1]
        horario = result[6]
        print(dia,horario,"$$$$$$$$$$$",data,horas)
            
        if dia == data and horario != None:
          
          resp = {"status":"erro"}
          
          return resp 
  

      print("Efetuando Saida")
      
      cursor.execute("""UPDATE {} SET Cafe_entra=? WHERE Data=?""".format(cpf3),(horas,data))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      
      print('sou verificassss',verifica_entradas)
      
      resp = {"status":"Saida para café com sucesso!!"}
      
      return resp
    
    elif botao == "Retorno café":
      print("Saida",botao)
      for result in verifica_entrada:
        print(result)
        dia = result[1]
        horario = result[7]
        print(dia,horario,"$$$$$$$$$$$",data,horas)
            
        if dia == data and horario != None:
          
          resp = {"status":"erro"}        
          return resp 
  

      print("Efetuando Saida")
      
      cursor.execute("""UPDATE {} SET Cafe_saida=? WHERE Data=?""".format(cpf3),(horas,data))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      
      print('sou verificassss',verifica_entradas)
      
      resp = {"status":"Retorno do café com sucesso!!"}
      
      return resp
  
    elif botao == "Saída":
      print("Saida",botao)
      for result in verifica_entrada:
        print(result)
        dia = result[1]
        horario = result[3]
        print(dia,horario,"$$$$$$$$$$$",data,horas)
            
        if dia == data and horario != None:
          resp = {"status":"erro"}
          
          return resp 
  
      print("Efetuando Saida")
      
      cursor.execute("""UPDATE {} SET Saida=? WHERE Data=?""".format(cpf3),(horas,data))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      
      print('sou verificassss',verifica_entradas)
      
      resp = {"status":"Saida efetuada com sucesso!!"}
      
      return resp

  else:
    resp = {"status":"Seu local não confere com endereço cadastrado no posto\nPor favor dirija-se para o mesmo local em que fez o cafadtro do posto !!"}
        
    return resp
