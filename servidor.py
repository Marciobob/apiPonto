import socket, threading, select
import time 


def client_conectado(client,endereco):
  print(f"O client se conectou do endereço {endereco}")
  servidor = socket.socket()
  servidor.connect(("localhost",8158))
  
  try:
    while True:
      leitura, escrita, erro = select.select([servidor, client], [], [servidor, client])
     
      #print("eu soub")
      
      if erro != []: raise

      for lendo in leitura:
        data = lendo.recv(1024).decode('UTF-8')
        #print("eiiiii",data)
        
       # if not data:raise
       # print("not")
        if data:
          print("sou data",data)
          print("resposta client")
          res = "okkki"
          servidor.send(res.encode('UTF-8'))
        
          soc.close()
        else:
          print("resposta 2")
          res = "okkki"
          servidor.send(res.encode('UTF-8'))
        
  except:
    print("Cliente desconectado",data)
    oi= "oi"
    client.send(oi.encode('UTF-8'))
   

HOST = '0.0.0.0'
PORT = 5000

soc = socket.socket(socket.AF_INET, socket .SOCK_STREAM)

soc.bind((HOST,PORT))
soc.listen(3)

print('Aguardando cliente')

while True:
  client, endereco = soc.accept()
  print('Conectado')
  
  threading.Thread(target=client_conectado, args=(client,endereco)).start()
  
     
     
     
	
	