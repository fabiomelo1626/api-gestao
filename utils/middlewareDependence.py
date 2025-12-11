from fastapi import Depends, HTTPException, status
from models.permissionTableModels import PermissionTable
from models.userModels import User
from models.userPermissionModels import UserPermission
from sqlalchemy.orm import Session
from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user



def check_permission(tabela_nome: str, acao: str):
    def wrapper(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        perm = (
            db.query(UserPermission)
            .filter(UserPermission.user_id == current_user["id"])
            .first()
        )

        if not perm:
            raise HTTPException(
                status_code=403,
                detail="Nenhuma permissão encontrada para o usuário"
            )

        tabela_ok = getattr(perm, tabela_nome, False)

        acao_ok = getattr(perm, acao, False)

        if not tabela_ok:
            raise HTTPException(
                status_code=403,
                detail=f"Usuário não possui permissão de acesso à tabela ({tabela_nome})"
            )

        if not acao_ok:
            raise HTTPException(
                status_code=403,
                detail=f"Usuário não possui permissão para {acao}"
            )

        return True

    return wrapper