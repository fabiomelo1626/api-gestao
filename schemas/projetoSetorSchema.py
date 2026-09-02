from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class ProjetoSetorSchema(BaseModel):
    user_id: Optional[int] = None
    local_id: Optional[int] = None

    setor_id: Optional[int] = None
    projeto_id: Optional[int] = None
    class Config:
        from_attributes = True

class ProjetoSetorCreate(ProjetoSetorSchema):
    pass

class ProjetoSetorResponse(ProjetoSetorSchema):
    id: int
