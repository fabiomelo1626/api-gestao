from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class PerfilSchema(BaseModel):
    user_id: int
    local_id: int
    descricao: Optional[str] = None

    class Config:
        from_attributes = True

class PerfilCreate(PerfilSchema):
    pass

    class Config:
        from_attributes = True
        
class PerfilResponse(PerfilSchema):
    id: int

    class Config: 
        from_attributes = True
