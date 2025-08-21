from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MaeSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
    CPF : Optional[int] = None
    Nome : Optional[str] = None
    DataNascimento : Optional[datetime] = None
    #Raca : Optional[int] = None
    QuantidadeConsulta : Optional[int] = None
    #GravidezRisco : Optional[int] = None

    
    class Config:
        from_attributes  : True
        
class MaeCreate(MaeSchema):
    pass 

    class Config:
        from_attributes  : True

class MaeResponse(MaeSchema):
    id: int
    
    class Config:
        from_attributes  : True
