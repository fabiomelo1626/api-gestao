from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.localAcessoModels import *
from models.acessoModels import Acesso
from models.solicitacaoProcedimentoAmbulatorialModels import SolicitacaoProcedimentoAmbulatorial
from schemas.solicitacaoProcedimentoAmbulatorialSchema import SolicitacaoProcedimentoAmbulatorialCreate, SolicitacaoProcedimentoAmbulatorialResponse
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import SQLAlchemyError


solicitacao_procedimento = APIRouter(prefix="/api")



@solicitacao_procedimento.post("/create-solicitacao-procedimento/", response_model=SolicitacaoProcedimentoAmbulatorialResponse)
def create_solicitacao_procedimento(
    solicitacao_procedimento: SolicitacaoProcedimentoAmbulatorialCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    try:
        db_solicitacao = SolicitacaoProcedimentoAmbulatorial(**solicitacao_procedimento.dict())
        db_solicitacao.data_registro = datetime.today()
        db.add(db_solicitacao)
        db.commit()
        db.refresh(db_solicitacao)
        return db_solicitacao
   

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@solicitacao_procedimento.get("/busca-solicitacao-procedimento/{solicitacao_id}", response_model=SolicitacaoProcedimentoAmbulatorialResponse)
def search_solicitacao_procedimento(solicitacao_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    solicicatacao = db.query(SolicitacaoProcedimentoAmbulatorial).filter(SolicitacaoProcedimentoAmbulatorial.id == solicitacao_id).first()
    if not solicicatacao:
        raise HTTPException(status_code=404, detail="Solicitacao Procedimento não encontrada")
    return solicicatacao



@solicitacao_procedimento.get("/solicitacoes-procedimentos", response_model=SolicitacaoProcedimentoAmbulatorialResponse)
def solicitacao_all(db:Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    solicitacoes = db.query(SolicitacaoProcedimentoAmbulatorial).all()

    return solicitacoes



@solicitacao_procedimento.get("/solicitacoes-by-local_id/{local_id}", response_model=SolicitacaoProcedimentoAmbulatorialResponse)
def search_solicitacao_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    solicitacoes = db.query(SolicitacaoProcedimentoAmbulatorial).filter(SolicitacaoProcedimentoAmbulatorial.local_id == local_id).first()
    if not solicitacoes:
        HTTPException(status_code=404, detail="Solicitacao Procedimento  não encontrado para o local")
    return solicitacoes



@solicitacao_procedimento.put("/editar-solicitacao-procedimento/{solicitacao_id}", response_model=SolicitacaoProcedimentoAmbulatorialResponse)
def update_solicitacao(
    solicitacao_id: int,
    solicitacao: SolicitacaoProcedimentoAmbulatorialCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_solicitacao = db.query(SolicitacaoProcedimentoAmbulatorial).filter(SolicitacaoProcedimentoAmbulatorial.id == solicitacao_id).first()

    if not db_solicitacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitacao Procedimento não encontrado")

    try:
        db_solicitacao = SolicitacaoProcedimentoAmbulatorial(**solicitacao.dict())
        db_solicitacao.data_alteracao = datetime.today()
        db.add(db_solicitacao)
        db.commit()
        db.refresh(db_solicitacao)
        return db_solicitacao
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
