from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EstabelecimentoLeitoSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
    CNES : Optional[int] = None
    #TipoLeito : Optional[int] = None
    Quantidade : Optional[int] = None
    QuantidadeSUS : Optional[int] = None
    
    class Config:
        from_attributes  : True
        
class EstabelecimentoLeitoCreate(EstabelecimentoLeitoSchema):
    pass 

    class Config:
        from_attributes  : True

class EstabelecimentoLeitoResponse(EstabelecimentoLeitoSchema):
    id: int
    
    class Config:
        from_attributes  : True
