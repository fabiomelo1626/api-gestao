from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.localAcessoModels import *
from models.acessoModels import Acesso
from models.estabelecimentoSaudeModels import EstabelecimentoSaude
from schemas.estabelecimentoSaudeSchema import EstabelecimentoSaudeCreate, EstabelecimentoSaudeResponse
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import SQLAlchemyError

estabelecimento = APIRouter(prefix="/api")



@estabelecimento.post("/create-estabelecimento-saude/", response_model=EstabelecimentoSaudeResponse)
def create_estabelecimento(
    estabelecimento: EstabelecimentoSaudeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    try:
        db_estabelecimento = EstabelecimentoSaude(**estabelecimento.dict())
        db_estabelecimento.data_registro = datetime.today()
        db.add(db_estabelecimento)
        db.commit()
        db.refresh(db_estabelecimento)
        return db_estabelecimento
   

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@estabelecimento.get("/busca-estabelecimento-saude/{estabelecimento_id}", response_model=EstabelecimentoSaudeResponse)
def search_estabelecimento(estabelecimento_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimento = db.query(EstabelecimentoSaude).filter(EstabelecimentoSaude.id == estabelecimento_id).first()
    if not estabelecimento:
        raise HTTPException(status_code=404, detail="Estabelecimento Divulgação não encontrada")
    return estabelecimento



@estabelecimento.get("/estabelecimentos-saude", response_model=EstabelecimentoSaudeResponse)
def estabelecimento_all(db:Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimentos = db.query(EstabelecimentoSaude).all()

    return estabelecimentos


@estabelecimento.get("/estabelecimentos-saude-by-local_id/{local_id}", response_model=EstabelecimentoSaudeResponse)
def search_estabelecimento_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimento = db.query(EstabelecimentoSaude).filter(EstabelecimentoSaude.local_id == local_id).first()
    if not estabelecimento:
        raise HTTPException(status_code=404, detail="Estabelecimento não encontrado para o local")
    return estabelecimento


@estabelecimento.put("/editar-estabelecimento-saude/{estabelecimento_id}", response_model=EstabelecimentoSaudeResponse)
def update_estabelecimento(
    estabelecimento_id: int,
    estabelecimento: EstabelecimentoSaudeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_estabelecimento = db.query(EstabelecimentoSaude).filter(EstabelecimentoSaude.id == estabelecimento_id).first()

    if not db_estabelecimento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estabelecimento não encontrada")

    try:
        db_estabelecimento = EstabelecimentoSaude(**estabelecimento.dict())
        db_estabelecimento.data_alteracao = datetime.today()
        db.add(db_estabelecimento)
        db.commit()
        db.refresh(db_estabelecimento)
        return db_estabelecimento
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
