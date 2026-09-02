from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class PermissionTablesSchema(BaseModel):
    user_id: Optional[int] = None
    local_id: Optional[int] = None
    data_registro: Optional[datetime] = None
    data_alteracao: Optional[datetime] = None

    nome : Optional[str] = None
    tabela_metas : Optional[bool] = None
    tabela_responsaveis : Optional[bool] = None
    tabela_tarefas : Optional[bool] = None
    tabela_setor : Optional[bool] = None
    tabela_pessoa : Optional[bool] = None
    tabela_atendimento : Optional[bool] = None
    tabela_acessos : Optional[bool] = None
    tabela_cargos : Optional[bool] = None
    tabela_projetos : Optional[bool] = None
    tabela_user : Optional[bool] = None
    tabela_permissoes: Optional[bool] = None
    tabela_projeto_setor: Optional[bool] = None

    listar: Optional[bool] = None
    criar: Optional[bool] = None
    editar: Optional[bool] = None
    deletar: Optional[bool] = None
    
    class Config:
        from_attributes = True

class PermissionTablesCreate(PermissionTablesSchema):
    pass

class PermissionTablesResponse(PermissionTablesSchema):
    id: int





class UserPermissionSchema(BaseModel):
    user_cadastra_id: Optional[int] = None

    user_id: Optional[int] = None
    local_id: Optional[int] = None
    permission_table_id: Optional[int] = None
    data_registro: Optional[datetime] = None
    data_alteracao: Optional[datetime] = None

   
    
    class Config:
        from_attributes = True

class UserPermissionCreate(UserPermissionSchema):
    pass

class UserPermissionResponse(UserPermissionSchema):
    id: int
