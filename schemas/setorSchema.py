from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class SetorSchema(BaseModel):
    #user_id: Optional[int] = None
    #local_id: Optional[int] = None

    data_registro: Optional[datetime] = None
    data_alteracao: Optional[datetime] = None
    descricao: Optional[str] = None
    class Config:
        from_attributes = True

class SetorCreate(SetorSchema):
    pass

class SetorResponse(SetorSchema):
    id: int
