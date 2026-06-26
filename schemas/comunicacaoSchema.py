from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime


class ComunicacaoSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    remetente_id : Optional[int] = None
    instituicao_id : Optional[int] = None
    destinatario_id : Optional[int] = None
    destino_instituicao_id : Optional[Union[int, List[int]]] = None
    categoria : Optional[int] = None
    titulo: Optional[str] = None
    conteudo: Optional[str] = None
    status: Optional[str] = None
    anexo: Optional[str] = None

    data_registro: Optional[datetime] = None
    data_alteracao: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
class ComunicacaoCreate(ComunicacaoSchema):
    pass 

    class Config:
        from_attributes = True

import uuid

class ComunicacaoResponse(ComunicacaoSchema):
    id: uuid.UUID
    
    class Config:
        from_attributes = True
