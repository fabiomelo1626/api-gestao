from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CoberturaVacinalSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
    FaixaEtaria : Optional[int] = None
    Vacina : Optional[int] = None
    QuantidadeMasculino : Optional[int] = None
    QuantidadeFeminino : Optional[int] = None
    
    class Config:
        from_attributes  : True
        
class CoberturaVacinalCreate(CoberturaVacinalSchema):
    pass 

    class Config:
        from_attributes  : True

class CoberturaVacinalResponse(CoberturaVacinalSchema):
    id: int
    
    class Config:
        from_attributes  : True
