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
    cpf : Optional[int] = None
    titulo : Optional[int] = None
    nome : Optional[str] = None
    datanascimento : Optional[datetime]
    cidade : Optional[str] = None
    estado : Optional[str] = None
    logradouro : Optional[str] = None
    numero : Optional[str] = None
    bairro : Optional[str] = None
    cep : Optional[int] = None
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

