from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class CargoSchema(BaseModel):
    user_id: Optional[int] = None
    local_id: Optional[int] = None

    data_registro: Optional[datetime] = None
    data_alteracao: Optional[datetime] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None
    class Config:
        from_attributes = True

class CargoCreate(CargoSchema):
    pass

class CargoResponse(CargoSchema):
    id: int
