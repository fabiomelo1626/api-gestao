from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.auxiliaresModels import *


auxiliares = APIRouter(prefix="/api")



@auxiliares.get("/status", summary="Listar Status")
def listar_status(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(Status).all()


