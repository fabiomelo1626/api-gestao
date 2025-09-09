from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class VinculoProfissionalSaudeSchema(BaseModel):
    user_id : Optional[int] = None
    local_id : Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
    CNES : Optional[int] = None
    CPF : Optional[int] = None
    Matricula : Optional[int] = None
<<<<<<< HEAD
    Vinculo : Optional[int] = None
=======
    Vinculo : Optional[str] = None
>>>>>>> cf3bda59fc7e0ba69ebeb6ce3a900f36767d9ece
    Ocupacao : Optional[int] = None
    CargaHorariaAmbulatorio : Optional[int] = None
    CargaHorariaTotal : Optional[int] = None
    DataInicioVinculo : Optional[datetime] = None
    DataFimVinculo : Optional[datetime] = None

    
    class Config:
        from_attributes  : True
        
class VinculoProfissionalSaudeCreate(VinculoProfissionalSaudeSchema):
    pass 

    class Config:
        from_attributes  : True

class VinculoProfissionalSaudeResponse(VinculoProfissionalSaudeSchema):
    id: int
    
    class Config:
        from_attributes  : True
