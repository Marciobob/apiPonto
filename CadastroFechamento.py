# encoding: utf-8
from flask import  Flask, request, jsonify
import os
import time
import json
import sqlite3
import hmac
import hashlib
import base64


def CadastroFechamento(jsonclient):
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
    
        resp = {"status": "ok"}  
        return resp