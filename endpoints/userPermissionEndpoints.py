from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.userModels import User
from models.userPermissionModels import UserPermission
from schemas.userPermissionSchema import UserPermissionCreate, UserPermissionResponse
from sqlalchemy.exc import SQLAlchemyError


permission = APIRouter()

@permission.post("/create-permissions", response_model=UserPermissionResponse)
def set_user_permission(
    permission: UserPermissionCreate,
    db: Session = Depends(get_db),
    #current_user: dict = Depends(get_current_user)
):
    try:
        db_permission = UserPermission(**permission.dict())
        db_permission.data_registro = datetime.today()
        #db_permission.local_id = current_user["acesso_id"]

        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)

        return db_permission
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


