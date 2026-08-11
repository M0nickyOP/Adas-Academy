from sqlite3 import IntegrityError
from fastapi import FastAPI, Depends, status,HTTPException
from typing import Annotated
from database import get_db,engine
from sqlalchemy.orm import Session
from schemas import  CreateContato
from models import Contato
import models

app = FastAPI()
models.Base.metadata.create_all(engine)

SessionDep = Annotated[Session,Depends(get_db)]

@app.get("/contatos/") #db é uma instancia de session, depends é uma injeção de dependencias
def listar_contatos(session:SessionDep): 
    return session.query(Contato).all() 

@app.post("/contatos/",status_code=201)
def create_contato(contato:CreateContato, session: SessionDep):
   novo_contato = Contato(**contato.model_dump()) # desempacota tudo oq tem na classe e transforma em um dicionário
   try: 
     session.add(novo_contato) # adiciona a sessão e deixa pendente para ser salva
     session.commit() # persiste a mudança
     session.refresh(novo_contato) # atualiza os dados e transforma em objetos python
     return novo_contato
   except IntegrityError:
     session.rollback()
   raise HTTPException(status_code=409,detail="Email já cadastrado")
    

@app.get("/contato/{id}/", response_model = CreateContato) 
def find_contato_by_id(id:int, session:SessionDep):
  contato = session.get(Contato,id)
  return contato

@app.delete("/contato/{id}/",status_code=status.HTTP_204_NO_CONTENT)
def delete_contato_by_id(id: int,session:SessionDep):
 contato = session.get(Contato,id)
 if contato is None:
    raise HTTPException(status_code = status.HTTP_404_NO_CONTENT, detail= "contato não encontrado")
 session.delete(contato)
 session.commit()
 return None

#
@app.patch("/contatos/{id}/",response_model = CreateContato)
def update_contato(id:int,dados:CreateContato, session:SessionDep):
   contato = session.get(Contato,id) # dando um get na sessão com contato
   if contato is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail="Contato não encontrado")
   for campo, valor in dados.model_dump().items(): 
      setattr(contato, campo, valor) #função nativa do python
   session.add(contato) # adiciona a mudança
   session.commit() # persiste a mudança
   session.refresh(contato) # atualiza os dados
   return contato


