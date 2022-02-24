from flask import  Flask, request, jsonify
import os
import time
import json
import sqlite3
import hmac
import hashlib
import base64


def EntradaManual(jsonclient):
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
                
                resp = {"status": "horario cadastrado com sucesso!!!"}

                return resp
        

            except sqlite3.Error as error:
                if error:
                    print(error)
                    resp = {"status": str(error)}

                    return resp
                
                
        
        elif verifica_entrada:
            print('sou verifasss',verifica_entrada)
            
            resp = {"status": "Desculpe, horario já cadastrado!!!"}

            return resp


        else:
            resp = {"status": "erro"}

            return resp
    
    except sqlite3.Error as error:
        if error : 
            print(error)
            resp = {"status": str(error)}

            return resp
    
