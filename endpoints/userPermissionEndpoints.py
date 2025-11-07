from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.userModels import User
from models.userPermissionModels import UserPermission
from schemas.userPermissionSchema import UserPermissionCreate, UserPermissionResponse
from models.permissionTableModels import PermissionTable
from schemas.permissionTableSchema import PermissionTableCreate
from endpoints.userEndpoints import get_current_user
from sqlalchemy.exc import SQLAlchemyError


permission = APIRouter()

@permission.post("/permissions/", response_model=UserPermissionResponse)
def set_user_permission(
    permission = UserPermissionCreate,
    table = PermissionTableCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == permission.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    tabela = db.query(PermissionTable).filter(PermissionTable.nome == table).first()

    perm = (
        db.query(UserPermission)
        .filter(UserPermission.user_id == permission.user_id, UserPermission.permission_table_id == tabela.id)
        .first()
    )

  

    perm.criar = permission.criar
    perm.listar = permission.listar
    perm.deletar = permission.deletar
    perm.editar = permission.editar
    perm.local_id = current_user["acesso_id"]

    db.add(perm)
    db.commit()
    db.refresh(perm)

    return {"message": f"Permissões atualizadas para {user.username}", "tabela": tabela.nome}
