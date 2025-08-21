from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.localAcessoModels import *
from models.acessoModels import Acesso
from models.vinculoProfissionalSaudeModels import VinculoProfissionalSaude
from schemas.vinculoProfissionalSaudeSchema import VinculoProfissionalSaudeCreate, VinculoProfissionalSaudeResponse
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import SQLAlchemyError

vinculo = APIRouter(prefix="/api")



@vinculo.post("/create-vinculo/", response_model=VinculoProfissionalSaudeResponse)
def create_vinculo(
    vinculo: VinculoProfissionalSaudeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    try:
        db_vinculo = VinculoProfissionalSaude(**vinculo.dict())
        db_vinculo.data_registro = datetime.today()
        db.add(db_vinculo)
        db.commit()
        db.refresh(db_vinculo)
        return db_vinculo
   

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@vinculo.get("/busca-vinculo/{vinculo_id}", response_model=VinculoProfissionalSaudeResponse)
def search_vinculo(vinculo_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimento = db.query(VinculoProfissionalSaude).filter(VinculoProfissionalSaude.id == vinculo_id).first()
    if not estabelecimento:
        raise HTTPException(status_code=404, detail="Vinculo profissional não encontrada")
    return estabelecimento



@vinculo.get("/vinculos", response_model=VinculoProfissionalSaudeResponse)
def vinculo_all(db:Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    vinculos = db.query(VinculoProfissionalSaude).all()

    return vinculos



@vinculo.get("/vinculos-by-local_id/{local_id}", response_model=VinculoProfissionalSaudeResponse)
def search_vinculo_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    vinculos = db.query(VinculoProfissionalSaude).filter(VinculoProfissionalSaude.local_id == local_id).first()
    if not vinculos:
        HTTPException(status_code=404, detail="Vinculo profissional  não encontrado para o local")
    return vinculos



@vinculo.put("/editar-vinculo/{vinculo_id}", response_model=VinculoProfissionalSaudeResponse)
def update_vinculo(
    vinculo_id: int,
    vinculo: VinculoProfissionalSaudeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_vinculo = db.query(VinculoProfissionalSaude).filter(VinculoProfissionalSaude.id == vinculo_id).first()

    if not db_vinculo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vinculo profissional não encontrado")

    try:
        db_vinculo = VinculoProfissionalSaude(**vinculo.dict())
        db_vinculo.data_alteracao = datetime.today()
        db.add(db_vinculo)
        db.commit()
        db.refresh(db_vinculo)
        return db_vinculo
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
