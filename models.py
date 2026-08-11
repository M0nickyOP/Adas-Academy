from sqlalchemy import  Column, Integer, String
from database import Base

class Contato(Base):
    __tablename__  = "Telefone"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    telefone = Column(String)
    email = Column(String, unique = True)
