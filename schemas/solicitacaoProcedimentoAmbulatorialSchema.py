from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SolicitacaoProcedimentoAmbulatorialSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
    CNES : Optional[int] = None
    Data : Optional[datetime] = None
    Procedimento : Optional[int] = None
    CID10Principal : Optional[str] = None
    CID10Secundario : Optional[str] = None
    CID10CausasAssociadas : Optional[str] = None
    Quantidade : Optional[int] = None
    Origem : Optional[str] = None
    Ocupacao : Optional[int] = None
    CPFSolicitante : Optional[int] = None
    
    class Config:
        from_attributes  : True
        
class SolicitacaoProcedimentoAmbulatorialCreate(SolicitacaoProcedimentoAmbulatorialSchema):
    pass 

    class Config:
        from_attributes  : True

class SolicitacaoProcedimentoAmbulatorialResponse(SolicitacaoProcedimentoAmbulatorialSchema):
    id: int
    
    class Config:
        from_attributes  : True
