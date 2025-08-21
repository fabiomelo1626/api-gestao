from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.localAcessoModels import *
from models.acessoModels import Acesso
from models.autorizacaoProcedimentoAmbulatorialModels import AutorizacaoProcedimentoAmbulatorial
from schemas.autorizacaoProcedimentoAmbulatorialSchema import AutorizacaoProcedimentoAmbulatorialCreate, AutorizacaoProcedimentoAmbulatorialResponse
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import SQLAlchemyError


autorizacao = APIRouter(prefix="/api")



@autorizacao.post("/create-autorizacao-leito/", response_model=AutorizacaoProcedimentoAmbulatorialResponse)
def create_autorizacao(
    autorizacao: AutorizacaoProcedimentoAmbulatorialCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    try:
        db_autorizacao = AutorizacaoProcedimentoAmbulatorial(**autorizacao.dict())
        db_autorizacao.data_registro = datetime.today()
        db.add(db_autorizacao)
        db.commit()
        db.refresh(db_autorizacao)
        return db_autorizacao
   

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@autorizacao.get("/busca-autorizacao/{autorizacao_id}", response_model=AutorizacaoProcedimentoAmbulatorialResponse)
def search_autorizacao(autorizacao_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    autorizacao = db.query(AutorizacaoProcedimentoAmbulatorial).filter(AutorizacaoProcedimentoAmbulatorial.id == autorizacao_id).first()
    if not autorizacao:
        raise HTTPException(status_code=404, detail="Autorizacao Procedimento não encontrada")
    return autorizacao



@autorizacao.get("/autorizacoes-procedimentos", response_model=AutorizacaoProcedimentoAmbulatorialResponse)
def autorizacoes_all(db:Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    autorizacoes = db.query(AutorizacaoProcedimentoAmbulatorial).all()

    return autorizacoes



@autorizacao.get("/autorizacoes-by-local_id/{local_id}", response_model=AutorizacaoProcedimentoAmbulatorialResponse)
def search_autorizacao_procedimento_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    autorizacoes_procedimentos = db.query(AutorizacaoProcedimentoAmbulatorial).filter(AutorizacaoProcedimentoAmbulatorial.local_id == local_id).first()
    if not autorizacoes_procedimentos:
        HTTPException(status_code=404, detail="Autorizacao Procedimentos não encontrados para o local")
    return autorizacoes_procedimentos



@autorizacao.put("/editar-autorizacao-proceidmento/{autorizacao_id}", response_model=AutorizacaoProcedimentoAmbulatorialResponse)
def update_autorizacao(
    autorizacao_id: int,
    autorizacao: AutorizacaoProcedimentoAmbulatorialCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_autorizacao = db.query(AutorizacaoProcedimentoAmbulatorial).filter(AutorizacaoProcedimentoAmbulatorial.id == autorizacao_id).first()

    if not db_autorizacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autorizacao Proceidmento não encontrada")

    try:
        db_autorizacao = AutorizacaoProcedimentoAmbulatorial(**autorizacao.dict())
        db_autorizacao.data_alteracao = datetime.today()
        db.add(db_autorizacao)
        db.commit()
        db.refresh(db_autorizacao)
        return db_autorizacao
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
