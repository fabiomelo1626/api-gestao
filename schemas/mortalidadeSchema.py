from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MortalidadeSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
     #FaixaEtaria : Optional[int] = None
    CategoriaCID : Optional[str] = None
    SubCategoriaCID : Optional[str] = None
    QuantidadeMasculino : Optional[int] = None
    QuantidadeFeminino : Optional[int] = None
    
    class Config:
        from_attributes  : True
        
class MortalidadeCreate(MortalidadeSchema):
    pass 

    class Config:
        from_attributes  : True

class MortalidadeResponse(MortalidadeSchema):
    id: int
    
    class Config:
        from_attributes  : True
