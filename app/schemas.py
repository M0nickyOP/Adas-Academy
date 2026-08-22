from pydantic import BaseModel



class CreateContato(BaseModel): 
    nome : str 
    telefone : str
    email : str
