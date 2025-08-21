from typing import Optional
from pydantic import BaseModel
from enum import Enum

class LocalAcessoSchema(BaseModel):
    nome: str
    cnpj: int
    Logradouro: str | None
    Numero: str | None
    Bairro: str | None
    CEP: int | None
    Cidade: str | None
    Estado: str | None
    email: Optional[str] = None
    telefone: Optional[int] = None

    logo: Optional[str] = None  
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True

class LocalAcessoCreate(LocalAcessoSchema):
    pass

class LocalAcessoResponse(LocalAcessoSchema):
    id: int