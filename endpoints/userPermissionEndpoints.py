from datetime import datetime
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
        db_permission = PermissionTables(**permission.dict())
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
