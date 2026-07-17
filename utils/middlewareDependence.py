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
        # Criamos os filtros dinâmicos baseados nas strings passadas
        filtro_tabela = getattr(PermissionTables, tabela_nome) == True
        filtro_acao = getattr(PermissionTables, acao) == True

        # Buscamos se existe QUALQUER permissão do usuário que atenda a ambos os critérios
        perm_valida = (
            db.query(PermissionTables)
            .join(UserPermissions, UserPermissions.permission_table_id == PermissionTables.id)
            .filter(
                UserPermissions.user_id == current_user["id"],
                filtro_tabela,
                filtro_acao
            )
            .first()
        )

        if not perm_valida:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Usuário não possui permissão para ({acao}) na tabela ({tabela_nome})."
            )

        return True

    return wrapper