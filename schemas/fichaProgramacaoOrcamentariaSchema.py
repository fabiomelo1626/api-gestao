from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FichaProgramacaoOrcamentariaSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
    CNES : Optional[int] = None
    Procedimento : Optional[int] = None
    Financiamento : Optional[str] = None
    Quantidade : Optional[int] = None
    ValorUnitario : Optional[float] = None
    ValorTotal : Optional[float] = None

    
    class Config:
        from_attributes  : True
        
class FichaProgramacaoOrcamentariaCreate(FichaProgramacaoOrcamentariaSchema):
    pass 

    class Config:
        from_attributes  : True

class FichaProgramacaoOrcamentariaResponse(FichaProgramacaoOrcamentariaSchema):
    id: int
    
    class Config:
        from_attributes  : True
