from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.localAcessoModels import *
from models.acessoModels import Acesso
from models.fichaProgramacaoOrcamentariaModels import FichaProgramacaoOrcamentaria
from schemas.fichaProgramacaoOrcamentariaSchema import FichaProgramacaoOrcamentariaCreate, FichaProgramacaoOrcamentariaResponse
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import SQLAlchemyError


ficha = APIRouter(prefix="/api")



@ficha.post("/create-ficha/", response_model=FichaProgramacaoOrcamentariaResponse)
def create_ficha(
    ficha: FichaProgramacaoOrcamentariaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    try:
        db_ficha = FichaProgramacaoOrcamentaria(**ficha.dict())
        db_ficha.data_registro = datetime.today()
        db.add(db_ficha)
        db.commit()
        db.refresh(db_ficha)
        return db_ficha
   

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@ficha.get("/busca-ficha/{ficha_id}", response_model=FichaProgramacaoOrcamentariaResponse)
def search_ficha(ficha_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ficha = db.query(FichaProgramacaoOrcamentaria).filter(FichaProgramacaoOrcamentaria.id == ficha_id).first()
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha Programacao não encontrada")
    return ficha



@ficha.get("/fichas", response_model=FichaProgramacaoOrcamentariaResponse)
def fichas_all(db:Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    fichas = db.query(FichaProgramacaoOrcamentaria).all()

    return fichas



@ficha.get("/fichas-by-local_id/{local_id}", response_model=FichaProgramacaoOrcamentariaResponse)
def search_fichas_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    fichas = db.query(FichaProgramacaoOrcamentaria).filter(FichaProgramacaoOrcamentaria.local_id == local_id).first()
    if not fichas:
        HTTPException(status_code=404, detail="Ficha programacao não encontrada para o local")
    return fichas



@ficha.put("/editar-ficha/{ficha_id}", response_model=FichaProgramacaoOrcamentariaResponse)
def update_ficha(
    ficha_id: int,
    ficha: FichaProgramacaoOrcamentariaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_ficha = db.query(FichaProgramacaoOrcamentaria).filter(FichaProgramacaoOrcamentaria.id == ficha_id).first()

    if not db_ficha:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ficha Programacao não encontrado")

    try:
        db_estabelecimento = FichaProgramacaoOrcamentaria(**ficha.dict())
        db_ficha.data_alteracao = datetime.today()
        db.add(db_ficha)
        db.commit()
        db.refresh(db_ficha)
        return db_ficha
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
