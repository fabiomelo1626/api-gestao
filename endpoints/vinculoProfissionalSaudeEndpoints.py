from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.vinculoProfissionalSaudeModels import VinculoProfissionalSaude
from schemas.vinculoProfissionalSaudeSchema import (
    VinculoProfissionalSaudeCreate,
    VinculoProfissionalSaudeResponse
)
from sqlalchemy.exc import SQLAlchemyError

vinculo = APIRouter(prefix="/api")


# Criar vínculo
@vinculo.post("/create-vinculo/", response_model=VinculoProfissionalSaudeResponse)
def create_vinculo(
    vinculo: VinculoProfissionalSaudeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_vinculo = VinculoProfissionalSaude(**vinculo.dict())
        db_vinculo.data_registro = datetime.today()
        db_vinculo.user_id = current_user["id"]
        # db_vinculo.local_id = current_user["acesso_id"]
        db.add(db_vinculo)
        db.commit()
        db.refresh(db_vinculo)
        return db_vinculo
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


# Buscar vínculo por ID
@vinculo.get("/busca-vinculo/{vinculo_id}", response_model=VinculoProfissionalSaudeResponse)
def search_vinculo(vinculo_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    vinculo = db.query(VinculoProfissionalSaude).filter(VinculoProfissionalSaude.id == vinculo_id).first()
    if not vinculo:
        raise HTTPException(status_code=404, detail="Vínculo profissional não encontrado")
    return vinculo


# Listar todos os vínculos
@vinculo.get("/vinculos", response_model=List[VinculoProfissionalSaudeResponse])
def list_vinculos(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    vinculos = db.query(VinculoProfissionalSaude).all()
    return vinculos


# Buscar vínculos por local
@vinculo.get("/vinculos-by-local_id/{local_id}", response_model=List[VinculoProfissionalSaudeResponse])
def list_vinculos_by_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    vinculos = db.query(VinculoProfissionalSaude).filter(VinculoProfissionalSaude.local_id == local_id).all()
    if not vinculos:
        raise HTTPException(status_code=404, detail="Nenhum vínculo profissional encontrado para o local")
    return vinculos


# Editar vínculo
@vinculo.put("/editar-vinculo/{vinculo_id}", response_model=VinculoProfissionalSaudeResponse)
def update_vinculo(
    vinculo_id: int,
    vinculo_data: VinculoProfissionalSaudeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_vinculo = db.query(VinculoProfissionalSaude).filter(VinculoProfissionalSaude.id == vinculo_id).first()
    if not db_vinculo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vínculo profissional não encontrado")
    
    try:
        # Atualiza somente os campos enviados
        for key, value in vinculo_data.dict(exclude_unset=True).items():
            setattr(db_vinculo, key, value)
        db_vinculo.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_vinculo)
        return db_vinculo
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
