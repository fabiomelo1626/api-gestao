from fastapi import Depends, HTTPException, status
from models.permissionTableModels import PermissionTable
from models.userModels import User
from models.userPermissionModels import UserPermission
from sqlalchemy.orm import Session
from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user



def check_permission(tabela_nome: str,  acao: str):
    def wrapper(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        perm = (
             db.query(UserPermission)
            .join(PermissionTable)
            .filter(PermissionTable.nome == tabela_nome, UserPermission.user_id == current_user.id)
            .first()
        )

        if not perm or not getattr(perm, f"can_{acao}", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Usuário não possui permissão para {acao}"
            )
        return True
    return wrapper
