from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.PermissionModels import PermissionTables, UserPermissions

def check_permission(tabela_nome: str, acao: str):
    def wrapper(
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        perm = (
            db.query(PermissionTables)
            .join(UserPermissions, UserPermissions.permission_table_id == PermissionTables.id)
            .filter(UserPermissions.user_id == current_user["id"])
            .first()
        )

        if not perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nenhuma permissão configurada para o seu usuário."
            )

        tabela_ok = getattr(perm, tabela_nome, False)
        acao_ok = getattr(perm, acao, False)

        if not tabela_ok:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Usuário não possui permissão de acesso à tabela ({tabela_nome})"
            )

        if not acao_ok:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Usuário não possui permissão para executar a ação ({acao})"
            )

        return True

    return wrapper