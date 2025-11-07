from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class PermissionTableSchema(BaseModel):
    nome: Optional[str] = None
    
    class Config:
        from_attributes = True

class PermissionTableCreate(PermissionTableSchema):
    pass

class PermissionTableResponse(PermissionTableSchema):
    id: int