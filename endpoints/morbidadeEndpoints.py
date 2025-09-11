from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.morbidadeModels import Morbidade
from schemas.morbidadeSchema import MorbidadeCreate, MorbidadeResponse

morbidade = APIRouter(prefix="/api")


@morbidade.post("/create-morbidade/", response_model=MorbidadeResponse)
def create_morbidade(
    morbidade_in: MorbidadeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_morbidade = Morbidade(**morbidade_in.dict())
        db_morbidade.data_registro = datetime.today()
        db_morbidade.user_id = current_user["id"]
        # db_morbidade.local_id = current_user.get("acesso_id")
        db.add(db_morbidade)
        db.commit()
        db.refresh(db_morbidade)
        return db_morbidade

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@morbidade.get("/busca-morbidade/{morbidade_id}", response_model=MorbidadeResponse)
def search_morbidade(
    morbidade_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_morbidade = db.query(Morbidade).filter(Morbidade.id == morbidade_id).first()
    if not db_morbidade:
        raise HTTPException(status_code=404, detail="Morbidade não encontrada")
    return db_morbidade


@morbidade.get("/morbidades", response_model=List[MorbidadeResponse])
def morbidades_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Morbidade).all()


@morbidade.get("/morbidades-by-local_id/{local_id}", response_model=List[MorbidadeResponse])
def search_morbidade_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    morbidades = db.query(Morbidade).filter(Morbidade.local_id == local_id).all()
  
    return morbidades


@morbidade.put("/editar-morbidade/{morbidade_id}", response_model=MorbidadeResponse)
def update_morbidade(
    morbidade_id: int,
    morbidade_in: MorbidadeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_morbidade = db.query(Morbidade).filter(Morbidade.id == morbidade_id).first()
    if not db_morbidade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Morbidade não encontrada")

    try:
        for key, value in morbidade_in.dict(exclude_unset=True).items():
            setattr(db_morbidade, key, value)

        db_morbidade.data_alteracao = datetime.today()
        db.commit()
        db.refresh(db_morbidade)
        return db_morbidade

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
