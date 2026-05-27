from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserSimple(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class LocalAcessoSimple(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


class AcessoCreate(BaseModel):
    usuario_id: int
    localacesso_id: int


class AcessoResponse(BaseModel):
    id: int
    usuario_id: int
    localacesso_id: int
    data_registro: Optional[date]
    data_alteracao: Optional[date]
    ativo: Optional[bool] = True

    usuarios: Optional[UserSimple] = None  
    locais: Optional[LocalAcessoSimple] = None

    class Config:
        from_attributes = True
        

class FirstPassword(BaseModel):
    username: str
    old_password: str
    new_password: str
