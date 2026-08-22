from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, declarative_base, sessionmaker



Engine = create_engine("sqlite:///./banco.db")
SessionLocal = sessionmaker(bind=Engine)
Base = declarative_base()



def get_db():
    db = SessionLocal() # chamando as conexões 
    try: 
        yield db #abre uma nova sessão no banco, o yield transforma a função em um generator, 
        #o yield pausa a sessão, guarda os dados e retorna a sessão
    finally:  # garante que o banco feche o banco
        db.close() #encerra a sessão