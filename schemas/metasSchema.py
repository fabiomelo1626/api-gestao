from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from schemas.tarefasSchema import TarefaResponse



class MetaSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None
    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None

    data_conclusao: Optional[datetime] = None
    projeto_id : Optional[int] = None
    setor : Optional[int] = None
    nome : Optional[str] = None
    descricao : Optional[str] = None
    responsavel : Optional[int] = None
    status : Optional[str] = None
    class Config:
        from_attributes = True

class MetaCreate(MetaSchema):
    pass

class MetaResponse(MetaSchema):
    id: int
    
    tarefa: list[TarefaResponse] = []
