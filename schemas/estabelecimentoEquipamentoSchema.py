from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EstabelecimentoEquipamentoSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
    CNES : Optional[int] = None
    Codigo : Optional[int] = None
    #Tipo : Optional[int] = None
    Quantidade : Optional[int] = None
    QuantidadeSUS : Optional[int] = None
    #DisponibilidadeSUS : Optional[int] = None
    
    class Config:
        from_attributes  : True
        
class EstabelecimentoEquipamentoCreate(EstabelecimentoEquipamentoSchema):
    pass 

    class Config:
        from_attributes  : True

class EstabelecimentoEquipamentoResponse(EstabelecimentoEquipamentoSchema):
    id: int
    
    class Config:
        from_attributes  : True
