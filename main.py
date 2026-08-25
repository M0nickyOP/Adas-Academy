from fastapi import FastAPI, Depends
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, declarative_base, sessionmaker

app = FastAPI()
engine = create_engine("sqlite:///./banco.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class CreateContato(BaseModel): 
    nome : str 
    telefone : str
    email : str

class Contato(Base):
    __tablename__  = "Telefone"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    telefone = Column(String)
    email = Column(String)



Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal() # chamando as conexões 
    try: 
        yield db #abre uma nova sessão no banco, o yield transforma a função em um generator, 
        #o yield pausa a sessão, guarda os dados e retorna a sessão
    finally:  # garante que o banco feche o banco
        db.close() #encerra a sessão

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

# mesmo erro, mas não sei o que e
@app.patch("/contatos/{id}/",response_model = CreateContato)
def update_contato(id:int,contato:CreateContato, session:SessionDep):
   contato = session.get(contato,id)
   contato_data = contato.model_dump()
   contato.sqlmodel_update(contato_data)
   session.add(contato)
   session.commit()
   session.refresh(contato)
   return contato

