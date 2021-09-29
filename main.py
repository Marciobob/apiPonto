from fastapi import FastAPI  
from fastapi import FastAPI  
from fastapi.responses import JSONResponse
import json


app = FastAPI()

@app.get('/user')
def user():
  print("logado")
  retorno = {"nome":"marcio"}
  ret= json.dumps(retorno)
  print(type(retorno))
  return retorno
  #return JSONResponse(content=ret, media_type="application/json")
  