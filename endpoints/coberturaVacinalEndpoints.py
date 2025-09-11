from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.coberturaVacinalModels import CoberturaVacinal
from schemas.coberturaVacinalSchema import CoberturaVacinalCreate, CoberturaVacinalResponse

cobertura = APIRouter(prefix="/api")


@cobertura.post("/create-cobertura-vacinal/", response_model=CoberturaVacinalResponse)
def create_cobertura_vacinal(
    cobertura_in: CoberturaVacinalCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_cobertura = CoberturaVacinal(**cobertura_in.dict())
        db_cobertura.data_registro = datetime.today()
        db_cobertura.user_id = current_user["id"]
        # db_cobertura.local_id = current_user["acesso_id"]
        db.add(db_cobertura)
        db.commit()
        db.refresh(db_cobertura)
        return db_cobertura
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@cobertura.get("/busca-cobertura-vacinal/{cobertura_id}", response_model=CoberturaVacinalResponse)
def search_cobertura_vacinal(
    cobertura_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_cobertura = db.query(CoberturaVacinal).filter(CoberturaVacinal.id == cobertura_id).first()
    if not db_cobertura:
        raise HTTPException(status_code=404, detail="Cobertura Vacinal não encontrada")
    return db_cobertura


@cobertura.get("/coberturas-vacinais", response_model=List[CoberturaVacinalResponse])
def cobertura_vacinal_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    coberturas = db.query(CoberturaVacinal).all()
    return coberturas


@cobertura.get("/coberturas-vacinais-by-local_id/{local_id}", response_model=List[CoberturaVacinalResponse])
def search_cobertura_vacinal_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    coberturas = db.query(CoberturaVacinal).filter(CoberturaVacinal.local_id == local_id).all()
  
    return coberturas


@cobertura.put("/editar-cobertura-vacinal/{cobertura_id}", response_model=CoberturaVacinalResponse)
def update_cobertura_vacinal(
    cobertura_id: int,
    cobertura_in: CoberturaVacinalCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_cobertura = db.query(CoberturaVacinal).filter(CoberturaVacinal.id == cobertura_id).first()
    if not db_cobertura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cobertura Vacinal não encontrada")

    try:
        # Atualiza apenas os campos enviados
        for key, value in cobertura_in.dict(exclude_unset=True).items():
            setattr(db_cobertura, key, value)

        db_cobertura.data_alteracao = datetime.today()
        db_cobertura.user_id = current_user["id"]
        db.commit()
        db.refresh(db_cobertura)
        return db_cobertura
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
