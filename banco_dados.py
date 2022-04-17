# encoding: utf-8
import sqlite3
from time import strftime


login = 'funcionarios'
cpf2 = 'fechamento'
adm = "encarregados"

#inicia o banco de dados de usuarios
conecxao = sqlite3.connect('usuarios.db')
cursor = conecxao.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS {}(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                           Nome TEXT NOT NULL,
                           Cpf TEXT NOT NULL,
                           Fone TEXT NOT NULL,
                           Token TEXT NOT NULL,
                           Email CHARSET utf8,
                           Senha TEXT NOT NULL);""".format(login))

cursor.execute("""CREATE TABLE IF NOT EXISTS {}(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                           Nome TEXT NOT NULL,
                           Cpf TEXT NOT NULL,
                           Fone TEXT NOT NULL,
                           Token TEXT NOT NULL,
                           Email CHARSET utf8,
                           Senha TEXT NOT NULL);""".format(adm))
                           

                           
cursor.execute("""CREATE TABLE IF NOT EXISTS {}(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Cpf TEXT,
    Datainicio TEXT,
    Datafechamento TEXT,
    Entrada TEXT,
    Almoco_entra TEXT,
    Almoco_saida TEXT,
    Cafe_entra TEXT,
    Cafe_saida TEXT,
    Saida TEXT,
    Sabado TEXT,
    Semanal TEXT);""".format(cpf2))
                           
                           
print('conectado ao banco de dados')


#cursor.execute("""SELECT * FROM cpf777""" )

#verifica_entrada = cursor.fetchone()
#print(verifica_entrada)




















