from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine("sqlite:///./banco.db")
SessionLocal = sessionmaker(bind=engine)
def get_db():
    db = SessionLocal() # chamando as conexões 
    try: 
        yield db #abre uma nova sessão no banco, o yield transforma a função em um generator, 
        #o yield pausa a sessão, guarda os dados e retorna a sessão
    finally:  # garante que o banco feche o banco
        db.close() #encerra a sessão