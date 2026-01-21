from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.userPermissionModels import UserPermission
from schemas.userPermissionSchema import UserPermissionCreate, UserPermissionResponse


permission = APIRouter(
    prefix="/api",
)



@permission.post("/create-permission/", response_model=UserPermissionResponse)
def create_permission(
    permission: UserPermissionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    local_id = permission.local_id
    if not local_id:
       raise HTTPException(status_code=403, detail="Local não encontrado no token ou na requisição.")
    
    try:
        db_permission = UserPermission(**permission.dict())
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



@permission.get("/permissions-by-user_id/{user_id}")
def search_permission_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    permissions = db.query(UserPermission).filter(UserPermission.user_id == user_id).all()
   
    return permissions
