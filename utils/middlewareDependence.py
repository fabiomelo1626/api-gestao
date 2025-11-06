from fastapi import Depends, HTTPException, status
from models.userModels import User
from models.userPermissionModels import UserPermission
from sqlalchemy.orm import Session
from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user



def check_permission(action: str):
    def wrapper(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        perm = (
            db.query(UserPermission)
            .filter(UserPermission.user_id == current_user.id)
            .first()
        )

        if not perm or not getattr(perm, f"can_{action}", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Usuário não possui permissão para {action}"
            )
        return True
    return wrapper
