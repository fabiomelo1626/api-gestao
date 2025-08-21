from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.localAcessoModels import *
from models.acessoModels import Acesso
from models.estabelecimentoLeitoModels import EstabelecimentoLeito
from schemas.estabelecimentoLeitoSchema import EstabelecimentoLeitoCreate, EstabelecimentoLeitoResponse
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import SQLAlchemyError

estabelecimento_leito = APIRouter(prefix="/api")



@estabelecimento_leito.post("/create-estabelecimento-leito/", response_model=EstabelecimentoLeitoResponse)
def create_estabelecimento(
    estabelecimento_leito: EstabelecimentoLeitoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    try:
        db_estabelecimento_leito = EstabelecimentoLeito(**estabelecimento_leito.dict())
        db_estabelecimento_leito.data_registro = datetime.today()
        db.add(db_estabelecimento_leito)
        db.commit()
        db.refresh(db_estabelecimento_leito)
        return db_estabelecimento_leito
   

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@estabelecimento_leito.get("/busca-estabelecimento_leito/{estabelecimento_leito_id}", response_model=EstabelecimentoLeitoResponse)
def search_estabelecimento(estabelecimento_leito_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimento_leito = db.query(EstabelecimentoLeito).filter(EstabelecimentoLeito.id == estabelecimento_leito_id).first()
    if not estabelecimento_leito:
        raise HTTPException(status_code=404, detail="Estabelecimento leito não encontrado")
    return estabelecimento_leito



@estabelecimento_leito.get("/estabelecimento_leitos", response_model=EstabelecimentoLeitoResponse)
def estabelecimento_leitos_all(db:Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimento_leitos = db.query(EstabelecimentoLeito).all()

    return estabelecimento_leitos



@estabelecimento_leito.get("/estabelecimento_leito-by-local_id/{local_id}", response_model=EstabelecimentoLeitoResponse)
def search_estabelecimento_leito_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimento_leitos = db.query(EstabelecimentoLeito).filter(EstabelecimentoLeito.local_id == local_id).first()
    if not estabelecimento_leitos:
        HTTPException(status_code=404, detail="Estabelecimento  Leito não encontrado para o local")
    return estabelecimento_leitos



@estabelecimento_leito.put("/editar-estabelecimento_leito/{estabelecimento_leito_id}", response_model=EstabelecimentoLeitoResponse)
def update_estabelecimento_leito(
    estabelecimento_leito_id: int,
    estabelecimento_leito: EstabelecimentoLeitoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_estabelecimento_leito = db.query(EstabelecimentoLeito).filter(EstabelecimentoLeito.id == estabelecimento_leito_id).first()

    if not db_estabelecimento_leito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estabelecimento Leito não encontrado")

    try:
        db_estabelecimento_leito = EstabelecimentoLeito(**estabelecimento_leito.dict())
        db_estabelecimento_leito.data_alteracao = datetime.today()
        db.add(db_estabelecimento_leito)
        db.commit()
        db.refresh(db_estabelecimento_leito)
        return db_estabelecimento_leito
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
