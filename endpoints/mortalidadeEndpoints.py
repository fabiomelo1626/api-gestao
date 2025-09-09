from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.mortalidadeModels import Mortalidade
from schemas.mortalidadeSchema import MortalidadeCreate, MortalidadeResponse
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import SQLAlchemyError


mortalidade = APIRouter(prefix="/api")



@mortalidade.post("/create-mortalidade/", response_model=MortalidadeResponse)
def create_mortalidade(
    mortalidade: MortalidadeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    try:
        db_mortalidade = Mortalidade(**mortalidade.dict())
        db_mortalidade.data_registro = datetime.today()
        db_mortalidade.user_id = current_user["id"]
        db_mortalidade.local_id = current_user["acesso_id"]
        db.add(db_mortalidade)
        db.commit()
        db.refresh(db_mortalidade)
        return db_mortalidade
   

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@mortalidade.get("/busca-mortalidade/{mortalidade_id}", response_model=MortalidadeResponse)
def search_mmortalidade(mortalidade_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    mortalidade = db.query(Mortalidade).filter(Mortalidade.id == mortalidade_id).first()
    if not mortalidade:
        raise HTTPException(status_code=404, detail="Mortalidade não encontrada")
    return mortalidade



@mortalidade.get("/mortalidades", response_model=MortalidadeResponse)
def mortalidade_all(db:Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    mortalidades = db.query(Mortalidade).all()

    return mortalidades



@mortalidade.get("/mortalidades-by-local_id/{local_id}", response_model=MortalidadeResponse)
def search_mortalidade_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    mortalidades = db.query(Mortalidade).filter(Mortalidade.local_id == local_id).first()
    if not mortalidades:
        HTTPException(status_code=404, detail="Mortalidade  não encontrada para o local")
    return mortalidades



@mortalidade.put("/editar-mortalidade/{mortalidade_id}", response_model=MortalidadeResponse)
def update_mortalidade(
    mortalidade_id: int,
    mortalidade: MortalidadeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_mortalidade = db.query(Mortalidade).filter(Mortalidade.id == mortalidade_id).first()

    if not db_mortalidade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mortalidade não encontrada")

    try:
        db_mortalidade = Mortalidade(**mortalidade.dict())
        db_mortalidade.data_alteracao = datetime.today()
        db.add(db_mortalidade)
        db.commit()
        db.refresh(db_mortalidade)
        return db_mortalidade
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
