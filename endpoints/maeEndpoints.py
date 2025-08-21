from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.localAcessoModels import *
from models.acessoModels import Acesso
from models.maeModels import Mae
from schemas.maeSchema import MaeCreate, MaeResponse
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import SQLAlchemyError


mae = APIRouter(prefix="/api")



@mae.post("/create-mae/", response_model=MaeResponse)
def create_mae(
    mae: MaeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    try:
        db_mae = Mae(**mae.dict())
        db_mae.data_registro = datetime.today()
        db.add(db_mae)
        db.commit()
        db.refresh(db_mae)
        return db_mae
   

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@mae.get("/busca-mae/{mae_id}", response_model=MaeResponse)
def search_mae(mae_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    mae = db.query(Mae).filter(Mae.id == mae_id).first()
    if not mae:
        raise HTTPException(status_code=404, detail="Mae não encontrada")
    return mae



@mae.get("/maes", response_model=MaeResponse)
def mae_all(db:Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    maes = db.query(Mae).all()

    return maes



@mae.get("/maes-by-local_id/{local_id}", response_model=MaeResponse)
def search_mae_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    maes = db.query(Mae).filter(Mae.local_id == local_id).first()
    if not maes:
        HTTPException(status_code=404, detail="Mae  não encontrada para o local")
    return maes



@mae.put("/editar-mae/{mae_id}", response_model=MaeResponse)
def update_mae(
    mae_id: int,
    mae: MaeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_mae = db.query(Mae).filter(Mae.id == mae_id).first()

    if not db_mae:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mae não encontrada")

    try:
        db_mae = Mae(**mae.dict())
        db_mae.data_alteracao = datetime.today()
        db.add(db_mae)
        db.commit()
        db.refresh(db_mae)
        return db_mae
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
