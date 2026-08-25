from fastapi import FastAPI, Depends
from typing import Annotated
from database import engine, get_db
from sqlalchemy.orm import Session
from schemas import  CreateContato
from models import Contato
import models

app = FastAPI()
models.Base.metadata.create_all(engine)

SessionDep = Annotated[Session,Depends(get_db)]
@app.get("/contatos/") #db é uma instancia de session, depends é uma injeção de dependencias
def listar_contatos(db:Session = Depends(get_db)): 
    return db.query(Contato).all() 

@app.post("/contatos/")
def create_contato(contato:CreateContato, db:Session = Depends(get_db)):
    novo_contato = Contato(**contato.model_dump()) # desempacota tudo oq tem na classe e transforma em um dicionário
    db.add(novo_contato) # adiciona a sessão e deixa pendente para ser salva
    db.commit() # persiste a mudança
    db.refresh(novo_contato) # atualiza os dados e transforma em objetos python
    return novo_contato

@app.get("/contato/{id}/", response_model = CreateContato) 
def find_contato_by_id(id:int, session:SessionDep):
  contato = session.get(Contato,id)
  return contato

@app.delete("/contato/{id}/")
def delete_contato_by_id(id: int,session:SessionDep):
 contato = session.get(Contato,id)
 session.delete(contato)
 session.commit()
 return {"mensagem" : "contato excluido com sucesso"}

#
@app.patch("/contatos/{id}/",response_model = CreateContato)
def update_contato(id:int,dados:CreateContato, session:SessionDep):
   contato = session.get(Contato,id) # dando um get na sessão com contato
   for campo, valor in dados.model_dump().items(): 
      setattr(contato, campo, valor) #função nativa do python
   session.add(contato) # adiciona a mudança
   session.commit() # persiste a mudança
   session.refresh(contato) # atualiza os dados
   return contato
