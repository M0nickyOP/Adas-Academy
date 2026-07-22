from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
lista_telefonica = []
class Contatos(BaseModel):
  nome: str
  contato: int

@app.post("/contatos")
def create_contact(contato:Contatos): 
  lista_telefonica.append(contato.dict())
  return contato

@app.get("/contatos")
def list_contact():
  return lista_telefonica
   
@app.get("/contatos/{nome}")
def contatos_by_name(nome:str):
  for contato in lista_telefonica:
    if contato["nome"] == nome:
      return contato


@app.delete("/contatos/{nome}")
def contatos_by_name(nome:str):
  for i, contato in enumerate(lista_telefonica):
    if contato["nome"] == nome:
      lista_telefonica.pop(i)
      return {"mensagem" : f"{nome} removido"}
  return HTTPException 

@app.put("/contatos/{contato_id}")
def update_contato(contato : Contatos)
  return {contato}