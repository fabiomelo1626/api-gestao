from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.mortalidadeModels import Mortalidade
from schemas.mortalidadeSchema import MortalidadeCreate, MortalidadeResponse

mortalidade = APIRouter(prefix="/api")


@mortalidade.post("/create-mortalidade/", response_model=MortalidadeResponse)
def create_mortalidade(
    mortalidade_in: MortalidadeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_mortalidade = Mortalidade(**mortalidade_in.dict())
        db_mortalidade.data_registro = datetime.today()
        db_mortalidade.user_id = current_user["id"]
        # db_mortalidade.local_id = current_user["acesso_id"]
        db.add(db_mortalidade)
        db.commit()
        db.refresh(db_mortalidade)
        return db_mortalidade

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@mortalidade.get("/busca-mortalidade/{mortalidade_id}", response_model=MortalidadeResponse)
def search_mortalidade(
    mortalidade_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_mortalidade = db.query(Mortalidade).filter(Mortalidade.id == mortalidade_id).first()
    if not db_mortalidade:
        raise HTTPException(status_code=404, detail="Registro de Mortalidade não encontrado")
    return db_mortalidade


@mortalidade.get("/mortalidades", response_model=List[MortalidadeResponse])
def mortalidades_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Mortalidade).all()


@mortalidade.get("/mortalidades-by-local_id/{local_id}", response_model=List[MortalidadeResponse])
def search_mortalidade_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    mortalidades = db.query(Mortalidade).filter(Mortalidade.local_id == local_id).all()
    return mortalidades


@mortalidade.put("/editar-mortalidade/{mortalidade_id}", response_model=MortalidadeResponse)
def update_mortalidade(
    mortalidade_id: int,
    mortalidade_in: MortalidadeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_mortalidade = db.query(Mortalidade).filter(Mortalidade.id == mortalidade_id).first()
    if not db_mortalidade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de Mortalidade não encontrado")

    try:
        # Atualiza somente os campos enviados
        for key, value in mortalidade_in.dict(exclude_unset=True).items():
            setattr(db_mortalidade, key, value)

        db_mortalidade.data_alteracao = datetime.today()
        db.commit()
        db.refresh(db_mortalidade)
        return db_mortalidade

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
