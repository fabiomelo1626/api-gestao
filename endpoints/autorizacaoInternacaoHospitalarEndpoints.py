from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.localAcessoModels import *
from models.acessoModels import Acesso
from models.autorizacaoInternacaoHospitalarModels import AutorizacaoInternacaoHospitalar
from schemas.autorizacaoInternacaoHospitalarSchema import AutorizacaoInternacaoHospitalarCreate, AutorizacaoInternacaoHospitalarResponse
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import SQLAlchemyError


autorizacao_internacao = APIRouter(prefix="/api")



@autorizacao_internacao.post("/create-autorizacao-internacao/", response_model=AutorizacaoInternacaoHospitalarResponse)
def create_autorizacao(
    autorizacao: AutorizacaoInternacaoHospitalarCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    

    try:
        db_autorizacao = AutorizacaoInternacaoHospitalar(**autorizacao.dict())
        db_autorizacao.user_id = current_user["id"]
        db_autorizacao.local_id = current_user["acesso_id"]
        db_autorizacao.data_registro = datetime.today()
        db.add(db_autorizacao)
        db.commit()
        db.refresh(db_autorizacao)
        return db_autorizacao
   

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@autorizacao_internacao.get("/busca-autorizacao-internacao/{autorizacao_id}", response_model=AutorizacaoInternacaoHospitalarResponse)
def search_autorizacao(autorizacao_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    autorizacao = db.query(AutorizacaoInternacaoHospitalar).filter(AutorizacaoInternacaoHospitalar.id == autorizacao_id).first()
    if not autorizacao:
        raise HTTPException(status_code=404, detail="Autorizacao internacao não encontrada")
    return autorizacao



@autorizacao_internacao.get("/autorizacoes-internacoes", response_model=AutorizacaoInternacaoHospitalarResponse)
def autorizacao_all(db:Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    autorizacoes = db.query(AutorizacaoInternacaoHospitalar).all()

    return autorizacoes



@autorizacao_internacao.get("/autorizacoes-by-local_id/{local_id}", response_model=AutorizacaoInternacaoHospitalarResponse)
def search_autorizacao_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    autorizacoes = db.query(AutorizacaoInternacaoHospitalar).filter(AutorizacaoInternacaoHospitalar.local_id == local_id).first()
    if not autorizacoes:
        HTTPException(status_code=404, detail="Autorizacao Internacao  não encontrada para o local")
    return autorizacoes



@autorizacao_internacao.put("/editar-autorizacao-internacao/{autorizacao_id}", response_model=AutorizacaoInternacaoHospitalarResponse)
def update_autorizacao(
    autorizacao_id: int,
    autorizacao: AutorizacaoInternacaoHospitalarCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_autorizacao = db.query(AutorizacaoInternacaoHospitalar).filter(AutorizacaoInternacaoHospitalar.id == autorizacao_id).first()

    if not db_autorizacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autorizacao Internacao não encontrada")

    try:
        db_autorizacao = AutorizacaoInternacaoHospitalar(**autorizacao.dict())
        db_autorizacao.data_alteracao = datetime.today()
        db.add(db_autorizacao)
        db.commit()
        db.refresh(db_autorizacao)
        return db_autorizacao
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
