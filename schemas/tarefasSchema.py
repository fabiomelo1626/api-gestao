from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class TarefaSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None
    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None

    data_conclusao: Optional[datetime] = None
    setor_id : Optional[int] = None
    Nome : Optional[str] = None
    descricao : Optional[str] = None
    responsavel : Optional[int] = None
    meta_id: Optional[int] = None
    status : Optional[str] = None
    
    class Config:
        from_attributes = True


class TarefaCreate(TarefaSchema):
    pass


class TarefaResponse(TarefaSchema):
    id: int


class TarefaUpdate(TarefaSchema):
    user_id : Optional[int] = None
    local_id : Optional[int] = None
    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None

    setor_id : Optional[int] = None
    Nome : Optional[str] = None
    descricao : Optional[str] = None
    responsavel : Optional[int] = None
    meta_id: Optional[int] = None
    status : Optional[str] = None
    class Config:
        from_attributes = True

