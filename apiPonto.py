from flask import  Flask, request, jsonify
import os
import time
import json
import sqlite3
import hmac
import hashlib
import base64


##instancia o flask
app = Flask(__name__)
#window = webview.create_window('Configurar posts', app)

@app.route("/test", methods=["GET"])
def test():
  resp = jsonify({"status": "olaaa"})

  resp.headers['Access-Control-Allow-Origin']='http://127.0.0.1:5000'
  return resp



#endpoint para encarregado de cadastrar entradas de funcionarios   
@app.route("/entradamanual", methods=["POST"])
def entradamanual():
  print("rota postos")
  #bodyss = request.get_json()
  #body= request.form.get('language')
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)
  print(jsonclient)
  
  cpf = jsonclient["cpf"]
  entrada = jsonclient["entrada"]
  
  saidaalmoco = jsonclient["saidaalmoco"]

  retornoalmoco = jsonclient["retornoalmoco"]
  saidacafe = jsonclient["saidacafe"]
  retornocafe = jsonclient["retornocafe"]
  saida = jsonclient["saida"]
  dataAtual = jsonclient["dataAtual"]

  if dataAtual[0] == '0':
   
    n = len(dataAtual)
    dataAtual = dataAtual[1:n]
    print('nova',dataAtual)

  print(dataAtual)

  cpf = cpf.replace(".", "")
  cpf = cpf.replace("-", "")
   
  cpf3 = str("cpf"+cpf)
  
 
  #conexao com banco dados
  conecxao = sqlite3.connect('usuarios.db')
  cursor = conecxao.cursor()
  print("Conectado ao banco de dados",dataAtual)

  try:
    cursor.execute("SELECT Data FROM {} WHERE Data={}".format(cpf3,dataAtual))
      
    verifica_entrada = cursor.fetchone()
    
    print('sou verifafff',verifica_entrada)
    
    if verifica_entrada == None:
      print('sou verifa',verifica_entrada)

      try:
        cursor.execute("""INSERT INTO {}(Data,Entrada,Saida,Almoco_entra,Almoco_saida,Cafe_entra,Cafe_saida) VALUES(?, ?, ?, ?, ?, ?, ?)""".format(cpf3), (dataAtual,entrada,saida,saidaalmoco,retornoalmoco,saidacafe,retornocafe))
        conecxao.commit()
           
        resp = jsonify({"status": "horario cadastrado com sucesso!!!"})

        resp.headers['Access-Control-Allow-Origin']='*'
        return resp
  

      except sqlite3.Error as error:
        if error : 
            print(error)
            resp = jsonify({"status": str(error)})

            resp.headers['Access-Control-Allow-Origin']='*'
            return resp
      
     
    
    elif verifica_entrada:
      print('sou verifasss',verifica_entrada)
        
      resp = jsonify({"status": "Desculpe, horario já cadastrado!!!"})

      resp.headers['Access-Control-Allow-Origin']='*'
      return resp


    else:
      resp = jsonify({"status": "erro"})

      resp.headers['Access-Control-Allow-Origin']='*'
      return resp
 
  except sqlite3.Error as error:
    if error : 
        print(error)
        resp = jsonify({"status": str(error)})

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
  
  token = jsonclient["token"]
  
  
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
  print("Conectado ao banco de dados")
  
  cursor.execute(f"SELECT * FROM {cpf3}")
  
  verifica_entrada = cursor.fetchall()
  
  print('sou verifa',verifica_entrada)
  lista_posto = verifica_entrada
  
  print(lista_posto)
  
  resp = jsonify({"status": lista_posto})

  resp.headers['Access-Control-Allow-Origin']='*'
  
  return resp




@app.route("/excluir_postos", methods=["POST"])
def excluir_postos():

  print("excluí postos")
 
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)
  print(jsonclient)
  
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
        
        resp = jsonify({"status": "Posto excluído com sucesso!!"})
        
        resp.headers['Access-Control-Allow-Origin']='*'
  
        return resp
        

    except sqlite3.Error as error:
        print("Falha ao excluir posto", error)
        
        resp = jsonify({"status": "Erro ao excluir posto!!"})

        resp.headers['Access-Control-Allow-Origin']='*'
  
        return resp

    finally:
        if conecxao:
            conecxao.close()
            print("banco de dados fechado")
  
  else:
    resp = jsonify({"status": "Posto inexistente!!"})
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
  
  token = jsonclient["token"]
  
  botao = jsonclient["botao"]
  endereco = jsonclient["endereco"]
  numero = jsonclient["numero"]
  hora = jsonclient["hora"]
  data = jsonclient["data"]
  
  data = data.replace("/","")
  
  horas = hora.replace(":","")
 
  print(token,endereco,numero,data,hora,botao)
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
  print("Conectado ao banco de dados")
  
  #cursor.execute(f"SELECT * FROM {cpf3}")
  cursor.execute(f"SELECT * FROM {cpf3}")
  
  verifica_entrada = cursor.fetchall()
  
  print('sou verifa',verifica_entrada)
  lista_posto = verifica_entrada
  
  print(lista_posto)
  
  if lista_posto == []:
    
    cursor.execute("""INSERT INTO {}(Data,Endereco,Numero) VALUES(?, ?, ?)""".format(cpf3), (data,endereco,numero))

    conecxao.commit()
    
    verifica_entrad = cursor.fetchall()
    
    print('sou verifahhhh',verifica_entrad)
    
  
    resp = jsonify({"status": "ok"})

    resp.headers['Access-Control-Allow-Origin']='*'
  
    return resp
  
  elif lista_posto != []:
   
    for res in lista_posto:
      print("sou ress",res[2])
      
      if res[2] == endereco:
        
          resp = jsonify({"status": "erro"})
          
          resp.headers['Access-Control-Allow-Origin']='*'
          
          return resp
      
      cursor.execute("""INSERT INTO {}(Data,Endereco,Numero) VALUES(?, ?, ?)""".format(cpf3), (data,endereco,numero))
      conecxao.commit()
  
      verifica_entrad = cursor.fetchall()
  
      print('sou veriftttth',verifica_entrad)
      
      resp = jsonify({"status": "ok"})

      resp.headers['Access-Control-Allow-Origin']='*'

      return resp
        
  else:
    resp = jsonify({"status": "erro"})

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
  
  cpf = jsonclient["cpf"]
  datainicio = jsonclient["datainicio"]
  datafechamento = jsonclient["datafechamento"]
  entrada = jsonclient["entrada"]
  saidaalmoco = jsonclient["saidaalmoco"]
  retornoalmoco = jsonclient["retornoalmoco"]
  saidacafe = jsonclient["saidacafe"]
  retornocafe = jsonclient["retornocafe"]
  saida = jsonclient["saida"]
  sabado = jsonclient["sabado"]
  semanal = jsonclient["semanal"]
  
  cpf = cpf.replace(".", "")
  cpf = cpf.replace("-", "")
  cpf2 = str("cpf"+cpf)
  
  print("eu sou sabado",cpf,sabado,semanal)
   #cria conexão ao banco

  conecxao = sqlite3.connect('usuarios.db')

  cursor = conecxao.cursor()
  print("Conectado ao banco de dados")
  
  #faz busca a usuário no banco 
  cursor.execute(f"SELECT * FROM fechamento WHERE Cpf={cpf}")
  verifica_entrada = cursor.fetchone()
  print(verifica_entrada)
  
  if verifica_entrada == None:

    print("Cadastrando usuario",type(saidacafe))
    
    dados = [( cpf,datainicio,datafechamento,entrada,saidaalmoco,retornoalmoco,saidacafe,retornocafe,saida,sabado,semanal)]
    
    cursor.executemany("""INSERT INTO fechamento(Cpf, Datainicio, Datafechamento, Entrada, Almoco_entra, Almoco_saida, Cafe_entra, Cafe_saida, Saida, Sabado, Semanal) VALUES(?,?,?,?,?,?,?,?,?,?,?)""", (dados))
    conecxao.commit()
  
    cursor.execute(f"SELECT * FROM fechamento WHERE Cpf={cpf}")

    verifica_entrada2 = cursor.fetchall()

    print(verifica_entrada2)
  
    resp = jsonify({"status": "ok"})
    resp.headers['Access-Control-Allow-Origin']='*'
  
    return resp
  

#rota principal envia dados json 
@app.route("/cadastro", methods=["POST"])
def loguin():
  print("cadasto")
  #bodyss = request.get_json()
  #body= request.form.get('language')
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)
  
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
  cursor.execute(f"SELECT * FROM funcionarios WHERE Cpf={cpf}")
 
 
  verifica_entrada = cursor.fetchone()
  
  print(verifica_entrada)
  
  if verifica_entrada == None:
    print("Cadastrando usuario")
    cursor.execute("""INSERT INTO funcionarios(Nome, Cpf, Fone, Token, Email, Senha) VALUES(?, ?, ?, ?, ?,?)""", (nome,cpf, fone, token, email, senha))
    conecxao.commit()
  
    cursor.execute("""CREATE TABLE IF NOT EXISTS {}(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Data TEXT,
    Entrada TEXT,
    Saida TEXT,
    Almoco_entra TEXT,
    Almoco_saida TEXT,
    Cafe_entra TEXT,
    Cafe_saida TEXT,
    Endereco TEXT,
    Numero TEXT);""".format(cpf2))
     
    cursor.execute("""CREATE TABLE IF NOT EXISTS {}(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Data TEXT,
    Entrada TEXT,
    Saida TEXT,
    Endereco TEXT,
    Numero TEXT);""".format(cpf3))
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS {}(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Data TEXT,
    Endereco TEXT,
    Numero TEXT);""".format(cpf4))
    
                           
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
    
    print(JWT)
    resp = jsonify({"token": JWT})
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp
   

  else:
    erro = jsonify({"status":"erro"})
    erro.headers['Access-Control-Allow-Origin']='*'
    print("erro")
    return erro


@app.route("/loguin", methods=["POST"])
def loguins():
  print("requestloguin")
  
  body = request.data
  decode = body.decode('utf-8')
  jsonclient = json.loads(decode)
  
  
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
      resp = jsonify({"token": JWT})
      resp.headers['Access-Control-Allow-Origin']='*'
      return resp
     
       
  except:
    resp = jsonify({"status":"erro"})
    resp.headers['Access-Control-Allow-Origin']='*'
    print("Erro!!")
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
    resp = jsonify({"status":"Você não tem bnenhum posto cadastrado!!"})
    resp.headers['Access-Control-Allow-Origin']='*'
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
          resp = jsonify({"status":"erro"})
          resp.headers['Access-Control-Allow-Origin']='*'
        
          return resp
    
      print("Entrada")
      cursor.execute("""INSERT INTO {}(Data,Entrada,Endereco,Numero) VALUES(?, ?, ?, ?)""".format(cpf3), (data,horas,endereco,numero))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      print('sou verifica',verifica_entradas)
      
      resp = jsonify({"status":"Entrada efetuada com sucesso!!"})
      resp.headers['Access-Control-Allow-Origin']='*'
      
      return resp
    
    elif botao == "Almoço":
      print("saindo para almoçar")
      for result in verifica_entrada:
            print(result)
            dia = result[1]
            horario = result[4]
            print(dia,horario,"$$$$$$$$$$$",data,horas)
            
            if dia == data and horario != None:
              resp = jsonify({"status":"erro"})
              resp.headers['Access-Control-Allow-Origin']='*'
            
              return resp
      print("Saindo para o almoço")
      cursor.execute("""UPDATE {} SET Almoco_entra=? WHERE Data=?""".format(cpf3),(horas,data))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      print('sou verificassss',verifica_entradas)
      resp = jsonify({"status":"Saida para o almoço efetuada com sucesso!!"})
      resp.headers['Access-Control-Allow-Origin']='*'
      
      return resp
    
    elif botao == "Retorno almoço":
      print("saindo para almoçar")
      for result in verifica_entrada:
        print(result)
        dia = result[1]
        horario = result[5]
        print(dia,horario,"$$$$$$$$$$$",data,horas)
            
        if dia == data and horario != None:
          resp = jsonify({"status":"erro"})
          resp.headers['Access-Control-Allow-Origin']='*'
          
          return resp
  
      print("Entrada")
      cursor.execute("""UPDATE {} SET Almoco_saida=? WHERE Data=?""".format(cpf3),(horas,data))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      
      print('sou verificassss',verifica_entradas)
      
      resp = jsonify({"status":"Retorno do almoço efetuado com sucesso!!"})
      resp.headers['Access-Control-Allow-Origin']='*'
      
      return resp
    
    elif botao == "Café":
      print("cafe",botao)
      for result in verifica_entrada:
        print(result)
        dia = result[1]
        horario = result[6]
        print(dia,horario,"$$$$$$$$$$$",data,horas)
            
        if dia == data and horario != None:
          
          resp = jsonify({"status":"erro"})
          resp.headers['Access-Control-Allow-Origin']='*'
          
          return resp 
  
      print("Efetuando Saida")
      
      cursor.execute("""UPDATE {} SET Cafe_entra=? WHERE Data=?""".format(cpf3),(horas,data))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      
      print('sou verificassss',verifica_entradas)
      
      resp = jsonify({"status":"Saida para café com sucesso!!"})
      resp.headers['Access-Control-Allow-Origin']='*'
      
      return resp
    
    elif botao == "Retorno café":
      print("Saida",botao)
      for result in verifica_entrada:
        print(result)
        dia = result[1]
        horario = result[7]
        print(dia,horario,"$$$$$$$$$$$",data,horas)
            
        if dia == data and horario != None:
          
          resp = jsonify({"status":"erro"})
          resp.headers['Access-Control-Allow-Origin']='*'
          
          return resp 
  
      print("Efetuando Saida")
      
      cursor.execute("""UPDATE {} SET Cafe_saida=? WHERE Data=?""".format(cpf3),(horas,data))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      
      print('sou verificassss',verifica_entradas)
      
      resp = jsonify({"status":"Retorno do café com sucesso!!"})
      resp.headers['Access-Control-Allow-Origin']='*'
      
      return resp
  
    elif botao == "Saída":
      print("Saida",botao)
      for result in verifica_entrada:
        print(result)
        dia = result[1]
        horario = result[3]
        print(dia,horario,"$$$$$$$$$$$",data,horas)
            
        if dia == data and horario != None:
          resp = jsonify({"status":"erro"})
          resp.headers['Access-Control-Allow-Origin']='*'
          
          return resp 
  
      print("Efetuando Saida")
      
      cursor.execute("""UPDATE {} SET Saida=? WHERE Data=?""".format(cpf3),(horas,data))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      
      print('sou verificassss',verifica_entradas)
      
      resp = jsonify({"status":"Saida efetuada com sucesso!!"})
      resp.headers['Access-Control-Allow-Origin']='*'
      
      return resp

  else:
    resp = jsonify({"status":"Seu local não confere com endereço cadastrado no posto\nPor favor dirija-se para o mesmo local em que fez o cafadtro do posto !!"})
    
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
  
  cpf3 = str("extra"+payload["cpf"])
  
  cpf_posto = str("posto"+payload["cpf"])
  
  #conexao com banco dados
  conecxao = sqlite3.connect('usuarios.db')
  cursor = conecxao.cursor()
  print("Conectado ao banco de dados")
  
  cursor.execute(f"SELECT * FROM {cpf_posto}")

  query_posto = cursor.fetchall()

  print("confere endereço",query_posto)
  
  if query_posto[0][2] == endereco:
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
          resp = jsonify({"status":"erro"})
          resp.headers['Access-Control-Allow-Origin']='*'
        
          return resp
    
      print("Entrada")
      cursor.execute("""INSERT INTO {}(Data,Entrada,Endereco,Numero) VALUES(?, ?, ?, ?)""".format(cpf3), (data,horas,endereco,numero))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      print('sou extra entrada',verifica_entradas)
      resp = jsonify({"status":"Entrada hora extra efetuada com sucesso!!"})
      resp.headers['Access-Control-Allow-Origin']='*'
      
      return resp
    
    elif botao == "Saída":
      print("Saida",botao)
      for result in verifica_entrada:
        print(result)
        dia = result[1]
        horario = result[3]
        print(dia,horario,"$$$$$$$$$$$",data,horas)
            
        if dia == data and horario != None:
          resp = jsonify({"status":"erro"})
          resp.headers['Access-Control-Allow-Origin']='*'
          
          return resp 
  
      print("Efetuando Saida")
      
      cursor.execute("""UPDATE {} SET Saida=? WHERE Data=?""".format(cpf3),(horas,data))
      conecxao.commit()
      
      cursor.execute(f"SELECT * FROM {cpf3}")
      verifica_entradas = cursor.fetchall()
      
      print('sou extra saida',verifica_entradas)
      
      resp = jsonify({"status":"Saida hora extra efetuada com sucesso!!"})
      resp.headers['Access-Control-Allow-Origin']='*'
      
      return resp
  else:
    resp = jsonify({"status":"Seu local não confere com endereço cadastrado no posto\nPor favor dirija-se para o mesmo local em que fez o cafadtro do posto !!"})
    
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


