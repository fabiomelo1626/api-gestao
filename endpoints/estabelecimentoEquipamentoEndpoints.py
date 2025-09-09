from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.localAcessoModels import *
from models.acessoModels import Acesso
from models.estabelecimentoEquipamentoModels import EstabelecimentoEquipamento
from schemas.estabelecimentoEquipamentoSchema import EstabelecimentoEquipamentoCreate, EstabelecimentoEquipamentoResponse
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import SQLAlchemyError

estabelecimento_equipamento = APIRouter(prefix="/api")



@estabelecimento_equipamento.post("/create-estabelecimento/", response_model=EstabelecimentoEquipamentoResponse)
def create_estabelecimento(
    estabelecimento: EstabelecimentoEquipamentoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    try:
        db_equipamento = EstabelecimentoEquipamento(**estabelecimento.dict())
        db_equipamento.data_registro = datetime.today()
        db_equipamento.user_id = current_user["id"]
        db_equipamento.local_id = current_user["acesso_id"]
        db.add(db_equipamento)
        db.commit()
        db.refresh(db_equipamento)
        return db_equipamento
   

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@estabelecimento_equipamento.get("/busca-estabelecimento/{estabelecimento_id}", response_model=EstabelecimentoEquipamentoResponse)
def search_estabelecimento(estabelecimento_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimento = db.query(EstabelecimentoEquipamento).filter(EstabelecimentoEquipamento.id == estabelecimento_id).first()
    if not estabelecimento:
        raise HTTPException(status_code=404, detail="Estebelecimento equipamento não encontrado")
    return estabelecimento



@estabelecimento_equipamento.get("/estabelecimentos", response_model=EstabelecimentoEquipamentoResponse)
def vinculo_all(db:Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimentos = db.query(EstabelecimentoEquipamento).all()

    return estabelecimentos



@estabelecimento_equipamento.get("/estabelecimentos-by-local_id/{local_id}", response_model=EstabelecimentoEquipamentoResponse)
def search_estabelecimento_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimentos = db.query(EstabelecimentoEquipamento).filter(EstabelecimentoEquipamento.local_id == local_id).first()
    if not estabelecimentos:
        HTTPException(status_code=404, detail="Estabelecimento equipamento  não encontrado para o local")
    return estabelecimentos



@estabelecimento_equipamento.put("/editar-estabelecimento/{estabelecimento_id}", response_model=EstabelecimentoEquipamentoResponse)
def update_estabelecimento(
    estabelecimento_id: int,
    vinculo: EstabelecimentoEquipamentoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_estabelecimento = db.query(EstabelecimentoEquipamento).filter(EstabelecimentoEquipamento.id == estabelecimento_id).first()

    if not db_estabelecimento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estabelecimento não encontrado")

    try:
        db_estabelecimento = EstabelecimentoEquipamento(**vinculo.dict())
        db_estabelecimento.data_alteracao = datetime.today()
        db.add(db_estabelecimento)
        db.commit()
        db.refresh(db_estabelecimento)
        return db_estabelecimento
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
