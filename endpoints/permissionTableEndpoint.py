from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.permissionTableModels import PermissionTable
from schemas.permissionTableSchema import PermissionTableCreate, PermissionTableResponse
from utils.middlewareDependence import check_permission


table = APIRouter(prefix="/api")


@table.get("/tabelas-by-local_id/{local_id}", response_model=List[PermissionTableResponse])
def search_tabelas_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tabelas = db.query(PermissionTable).filter(PermissionTable.local_id == local_id).all()
   
    return tabelas
