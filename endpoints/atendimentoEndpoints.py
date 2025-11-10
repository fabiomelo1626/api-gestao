from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.atendimentoModels import Atendimento
from schemas.atendimentoSchema import AtendimentnoCreate, AtendimentnoResponse

atendimento = APIRouter(prefix="/api")



@atendimento.post("/create-atendimento/", response_model=AtendimentnoResponse)
def create_atendimento(
    atendimento: AtendimentnoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_atendimento = Atendimento(**atendimento.dict())
        db_atendimento.data_registro = datetime.today()
        db_atendimento.user_id = current_user["id"]
        db_atendimento.local_id = current_user["acesso_id"]

        db.add(db_atendimento)
        db.commit()
        db.refresh(db_atendimento)
        return db_atendimento

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@atendimento.get("/busca-atendimento/{atendimento_id}", response_model=AtendimentnoResponse)
def search_atendimento(
    atendimento_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_atendimento = db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
    if not db_atendimento:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")
    return db_atendimento


@atendimento.get("/atendimentos", response_model=List[AtendimentnoResponse])
def atendimentos_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Atendimento).all()


@atendimento.get("/atendimentos-by-local_id/{local_id}", response_model=List[AtendimentnoResponse])
def search_pessoas_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    atendimentos = db.query(Atendimento).filter(Atendimento.local_id == local_id).all()
   
    return atendimentos


@atendimento.put("/editar-atendimentno/{atendimento_id}", response_model=AtendimentnoResponse)
def update_atendimento(
    atendimento_id: int,
    atendimento: AtendimentnoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_atendimento = db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
    if not db_atendimento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atendimento não encontrado")

    try:
        for key, value in atendimento.dict(exclude_unset=True).items():
            setattr(db_atendimento, key, value)

        db_atendimento.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_atendimento)
        return db_atendimento

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@atendimento.get("/atendimento-count-dia/{local_id}", response_model=AtendimentnoResponse)
def count_dia_atendimento(
    local_id: int,

    ):