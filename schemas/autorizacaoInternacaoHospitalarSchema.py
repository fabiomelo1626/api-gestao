from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AutorizacaoInternacaoHospitalarSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
    CNES : Optional[int] = None
    NumeroAIH : Optional[int] = None
    Identificacao : Optional[int] = None
    EspecialidadeLeito : Optional[int] = None
    ModalidadeInternacao : Optional[int] = None
    AIHAnterior : Optional[int] = None
    DataEmissao : Optional[datetime] = None
    DataInternacao : Optional[datetime] = None
    DataSaida : Optional[datetime] = None
    ProcedimentoSolicitado : Optional[int] = None
    CaraterInternacao : Optional[int] = None
    MotivoSaida : Optional[int] = None
    CNSSolicitante : Optional[int] = None
    CNSResponsavel : Optional[int] = None
    CNSAutorizador : Optional[int] = None
    DiagnosticoPrincipal : Optional[str] = None
    CNSPaciente : Optional[int] = None


    
    class Config:
        from_attributes  : True
        
class AutorizacaoInternacaoHospitalarCreate(AutorizacaoInternacaoHospitalarSchema):
    pass 

    class Config:
        from_attributes  : True

class AutorizacaoInternacaoHospitalarResponse(AutorizacaoInternacaoHospitalarSchema):
    id: int
    
    class Config:
        from_attributes  : True
