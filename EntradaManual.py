# encoding: utf-8
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
    
    print("+++++",cpf)
    
    entrada = jsonclient["entrada"]
    
    saidaalmoco = jsonclient["saidaalmoco"]

    retornoalmoco = jsonclient["retornoalmoco"]
    saidacafe = jsonclient["saidacafe"]
    retornocafe = jsonclient["retornocafe"]
    saida = jsonclient["saida"]
    datas = jsonclient["dataAtual"]
    
    dataAtual = datas.replace("/", "")
    dataAtual = datas.replace(".", "")
    
    cpf = cpf.replace(".", "")
    cpf = cpf.replace("-", "")
    
    cpf3 = str("cpf"+cpf)
    
    
    #conexao com banco dados
    conecxao = sqlite3.connect('usuarios.db')
    cursor = conecxao.cursor()
    print("Conectado ao banco de dados",dataAtual)
    
    query = f"SELECT * FROM {cpf3} WHERE Data LIKE '{dataAtual}'"
    try:
        cursor.execute(query)
        
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
    
