from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class AutorizacaoProcedimentoAmbulatorialSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
    CNES : Optional[int] = None
    CPFAutorizador : Optional[int] = None
    Ocupacao : Optional[int] = None
    CNS : Optional[int] = None
    Data : Optional[datetime] = None
    Procedimento : Optional[int] = None
    CID10Principal : Optional[str] = None
    CID10Secundario : Optional[str] = None
    CID10CausasAssociadas : Optional[str] = None
    Quantidade : Optional[int] = None
    Origem : Optional[str] = None
    
    class Config:
        from_attributes  : True
        
class AutorizacaoProcedimentoAmbulatorialCreate(AutorizacaoProcedimentoAmbulatorialSchema):
    pass 

    class Config:
        from_attributes  : True

class AutorizacaoProcedimentoAmbulatorialResponse(AutorizacaoProcedimentoAmbulatorialSchema):
    id: int
    
    class Config:
        from_attributes  : True
