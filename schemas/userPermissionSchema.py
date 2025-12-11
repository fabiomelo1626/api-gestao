from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class UserPermissionSchema(BaseModel):
    user_id: Optional[int] = None
    local_id: Optional[int] = None
    data_registro: Optional[datetime] = None
    data_alteracao: Optional[datetime] = None

    nome : Optional[str] = None
    tabela_pessoa : Optional[bool] = None
    tabela_pessoa_publica : Optional[bool] = None
    tabela_atendimento : Optional[bool] = None
    tabela_setor : Optional[bool] = None
    listar: Optional[bool] = None
    criar: Optional[bool] = None
    editar: Optional[bool] = None
    deletar: Optional[bool] = None
    
    class Config:
        from_attributes = True

class UserPermissionCreate(UserPermissionSchema):
    pass

class UserPermissionResponse(UserPermissionSchema):
    id: int
