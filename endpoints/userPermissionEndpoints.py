from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.PermissionModels import *
from schemas.userPermissionSchema import *

permission = APIRouter(
    prefix="/api",
)



@permission.post("/create-permission/", response_model=PermissionTablesResponse)
def create_permission(
    permission: PermissionTablesCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    local_id = permission.local_id
    if not local_id:
       raise HTTPException(status_code=403, detail="Local não encontrado no token ou na requisição.")
    
    try:
        db_permission = PermissionTables(**permission.model_dump())
        db_permission.user_id = current_user["id"]
        db_permission.data_registro = datetime.today()
        db_permission.local_id = local_id

        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@permission.get("/usuario/{usuario_id}/permissoes", response_model=list[PermissionTablesResponse])
def listar_permissoes_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    permissoes = (
        db.query(PermissionTables)
        .join(
            UserPermissions,
            UserPermissions.permission_table_id == PermissionTables.id
        )
        .filter(UserPermissions.user_id == usuario_id)
        .all()
    )

    return permissoes



@permission.get("/permission-by-local_id/{local_id}", response_model=List[PermissionTablesResponse])
def search_permissions_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    permissions = db.query(PermissionTables).filter(PermissionTables.local_id == local_id).all()
   
    return permissions


@permission.put("/editar-permission/{permission_id}", response_model=PermissionTablesResponse)
def update_permission_table(
    permission_id: int,
    permission: PermissionTablesCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_permission = db.query(PermissionTables).filter(PermissionTables.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="permission não encontrado")

    try:
        for key, value in permission.dict(exclude_unset=True).items():
            setattr(db_permission, key, value)

        db_permission.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_permission)
        return db_permission

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@permission.post("/create-user-permission/", response_model=UserPermissionResponse)
def create_user_permission(
    permission: UserPermissionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    local_id = permission.local_id
    if not local_id:
       raise HTTPException(status_code=403, detail="Local não encontrado no token ou na requisição.")
    
    try:
        db_permission = UserPermissions(**permission.model_dump())
        db_permission.user_cadastra_id = current_user["id"]
        db_permission.data_registro = datetime.today()
        db_permission.local_id = local_id

        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")




@permission.put("/editar-user-permission/{permission_id}", response_model=UserPermissionResponse)
def update_user_permission(
    permission_id: int,
    permission: UserPermissionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_permission = db.query(UserPermissions).filter(UserPermissions.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="permission não encontrado")

    try:
        for key, value in permission.dict(exclude_unset=True).items():
            setattr(db_permission, key, value)

        db_permission.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_permission)
        return db_permission

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@permission.get("/usuarios-permissoes-all", response_model=List[UserPermissionResponse])
def user_permissoes_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(UserPermissions).all()


@permission.delete("/editar-user-permission/{permission_id}")
def delete_user_permission(   
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_permission = db.query(UserPermissions).filter(UserPermissions.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Vínculo não encontrado")
    
    db.delete(db_permission)
    db.commit()
    return {"detail": "Vínculo removido com sucesso"}