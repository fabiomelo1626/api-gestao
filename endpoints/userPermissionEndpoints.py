from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.userModels import User
from models.userPermissionModels import UserPermission
from models.permissionTableModels import PermissionTable
from schemas.userPermissionSchema import UserPermissionCreate, UserPermissionResponse
from schemas.permissionTableSchema import PermissionTableCreate

# Agora o prefixo corresponde ao que o front-end usa: /api/permissions
permission = APIRouter(
    prefix="/api/permissions",
    tags=["permissions"]
)


# ------------------------------
# ROTA: CRIAR / ATUALIZAR PERMISSÃO DO USUÁRIO
# ------------------------------
@permission.post("/", response_model=UserPermissionResponse)
def set_user_permission(
    permission_data: UserPermissionCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Verifica se o usuário existe
        user = db.query(User).filter(User.id == permission_data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Verifica se a tabela de permissão existe
        table = db.query(PermissionTable).filter(
            PermissionTable.id == permission_data.permission_table_id
        ).first()

        if not table:
            raise HTTPException(status_code=404, detail="Tabela de permissão não encontrada")

        # Verifica se o registro de permissão já existe
        perm = (
            db.query(UserPermission)
            .filter(
                UserPermission.user_id == permission_data.user_id,
                UserPermission.permission_table_id == permission_data.permission_table_id
            )
            .first()
        )

        # Se já existir, atualiza
        if perm:
            perm.criar = permission_data.criar
            perm.listar = permission_data.listar
            perm.deletar = permission_data.deletar
            perm.editar = permission_data.editar
            perm.local_id = permission_data.local_id
        else:
            # Caso não exista, cria uma nova permissão
            perm = UserPermission(
                user_id=permission_data.user_id,
                permission_table_id=permission_data.permission_table_id,
                local_id=permission_data.local_id,
                criar=permission_data.criar,
                listar=permission_data.listar,
                editar=permission_data.editar,
                deletar=permission_data.deletar
            )
            db.add(perm)

        db.commit()
        db.refresh(perm)

        return {
            "id": perm.id,
            "user_id": perm.user_id,
            "permission_table_id": perm.permission_table_id,
            "local_id": perm.local_id,
            "listar": perm.listar,
            "criar": perm.criar,
            "editar": perm.editar,
            "deletar": perm.deletar,
            "table_name": table.nome
        }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar permissão: {str(e)}")


# ------------------------------
# ROTA: LISTAR PERMISSÕES POR USUÁRIO
# ------------------------------
@permission.get("/by-user/{user_id}")
def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    try:
        permissions = (
            db.query(UserPermission, PermissionTable)
            .join(PermissionTable, UserPermission.permission_table_id == PermissionTable.id)
            .filter(UserPermission.user_id == user_id)
            .all()
        )

        response = []
        for perm, table in permissions:
            response.append({
                "id": perm.id,
                "user_id": perm.user_id,
                "permission_table_id": perm.permission_table_id,
                "local_id": perm.local_id,
                "listar": perm.listar,
                "criar": perm.criar,
                "editar": perm.editar,
                "deletar": perm.deletar,
                "table_name": table.nome
            })

        return response

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar permissões: {str(e)}")
