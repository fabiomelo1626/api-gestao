from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class PessoaPublicaSchema(BaseModel):
    user_id: Optional[int] = None
    local_id: Optional[int] = None

    data_registro: Optional[datetime] = None
    data_alteracao: Optional[datetime] = None
    CPF: Optional[int] = None
    RG: Optional[int] = None
    Titulo: Optional[int] = None
    Nome: Optional[str] = None
    DataNascimento: Optional[datetime] = None
    Cidade: Optional[str] = None
    Estado: Optional[str] = None
    Logradouro: Optional[str] = None
    Numero: Optional[str] = None
    Bairro: Optional[str] = None
    CEP: Optional[int] = None
    email: Optional[str] = None
    # tipo: Optional[int] = None
    cargo_id: Optional[int] = None
    setor: Optional[int] = None
    
    class Config:
        from_attributes = True

class PessoaPublicaCreate(PessoaPublicaSchema):
    pass

class PessoaPublicaResponse(PessoaPublicaSchema):
    id: int
