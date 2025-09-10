from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.fichaProgramacaoOrcamentariaModels import FichaProgramacaoOrcamentaria
from schemas.fichaProgramacaoOrcamentariaSchema import (
    FichaProgramacaoOrcamentariaCreate,
    FichaProgramacaoOrcamentariaResponse
)

ficha = APIRouter(prefix="/api")


# Criar ficha
@ficha.post("/create-ficha/", response_model=FichaProgramacaoOrcamentariaResponse)
def create_ficha(
    ficha_in: FichaProgramacaoOrcamentariaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_ficha = FichaProgramacaoOrcamentaria(**ficha_in.dict())
        db_ficha.data_registro = datetime.today()
        db_ficha.user_id = current_user["id"]
        # db_ficha.local_id = current_user["acesso_id"]

        db.add(db_ficha)
        db.commit()
        db.refresh(db_ficha)
        return db_ficha

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


# Buscar ficha por ID
@ficha.get("/busca-ficha/{ficha_id}", response_model=FichaProgramacaoOrcamentariaResponse)
def search_ficha(
    ficha_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_ficha = db.query(FichaProgramacaoOrcamentaria).filter(FichaProgramacaoOrcamentaria.id == ficha_id).first()
    if not db_ficha:
        raise HTTPException(status_code=404, detail="Ficha Programação não encontrada")
    return db_ficha


# Listar todas as fichas
@ficha.get("/fichas", response_model=List[FichaProgramacaoOrcamentariaResponse])
def fichas_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(FichaProgramacaoOrcamentaria).all()


# Buscar fichas por local_id
@ficha.get("/fichas-by-local_id/{local_id}", response_model=List[FichaProgramacaoOrcamentariaResponse])
def search_fichas_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    fichas = db.query(FichaProgramacaoOrcamentaria).filter(FichaProgramacaoOrcamentaria.local_id == local_id).all()
   
    return fichas


# Editar ficha
@ficha.put("/editar-ficha/{ficha_id}", response_model=FichaProgramacaoOrcamentariaResponse)
def update_ficha(
    ficha_id: int,
    ficha_in: FichaProgramacaoOrcamentariaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_ficha = db.query(FichaProgramacaoOrcamentaria).filter(FichaProgramacaoOrcamentaria.id == ficha_id).first()
    if not db_ficha:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ficha Programação não encontrada")

    try:
        for key, value in ficha_in.dict(exclude_unset=True).items():
            setattr(db_ficha, key, value)

        db_ficha.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_ficha)
        return db_ficha

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
