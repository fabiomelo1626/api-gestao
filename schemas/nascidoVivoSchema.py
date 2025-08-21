from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class NascidoVivoSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
    CPFMae : Optional[int] = None
    NumeroDNV : Optional[int] = None
    #Raca : Optional[int] = None
    DataNascimento : Optional[datetime] = None
    #TipoParto : Optional[int] = None
    #TempoGestacao : Optional[int] = None
    PesoNascimento : Optional[float] = None
    
    class Config:
        from_attributes  : True
        
class NascidoVivoCreate(NascidoVivoSchema):
    pass 

    class Config:
        from_attributes  : True

class NascidoVivoResponse(NascidoVivoSchema):
    id: int
    
    class Config:
        from_attributes  : True
