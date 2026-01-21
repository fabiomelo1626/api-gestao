from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class ProjetoSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None
    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None

    data_conclusao: Optional[datetime] = None
    setor : Optional[int] = None
    Nome : Optional[str] = None
    descricao : Optional[str] = None
    responsavel : Optional[int] = None
    status : Optional[str] = None
    class Config:
        from_attributes = True

class ProjetoCreate(ProjetoSchema):
    pass

class ProjetoResponse(ProjetoSchema):
    id: int
