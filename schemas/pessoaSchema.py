from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from schemas.cargoSchema import CargoResponse
from schemas.setorSchema import SetorResponse



class PessoaSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
    CPF : Optional[int] = None
    RG : Optional[int] = None
    Titulo : Optional[int] = None
    Nome : Optional[str] = None
    DataNascimento : Optional[datetime]
    Cidade : Optional[str] = None
    Estado : Optional[str] = None
    Logradouro : Optional[str] = None
    Numero : Optional[str] = None
    Bairro : Optional[str] = None
    CEP : Optional[int] = None
    email : Optional[str] = None
    is_secretario : Optional[bool] = None
    is_funcionario : Optional[bool] = None
    setor_id : Optional[int] = None
    cargo_id : Optional[int] = None
    
    class Config:
        from_attributes = True

class PessoaCreate(PessoaSchema):
    pass

class PessoaResponse(PessoaSchema):
    id: int

    cargo: CargoResponse | None  
    setor: SetorResponse | None

    class Config:
        from_attributes = True

