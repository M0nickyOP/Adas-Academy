from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
lista_telefonica = []
class Contatos(BaseModel):
  nome: str
  contato: int

@app.post("/contatos")
def create_contato(item : Contatos):
  lista_telefonica.append(item)
  return lista_telefonica

@app.get("/contatos/{contato_id}")
def get_contato(contato_id : int) -> Contatos:
 if contato_id < len(lista_telefonica):
  return lista_telefonica[contato_id]
 else:
    raise HTTPException(status_code = 404, detail = "Item not found")


   