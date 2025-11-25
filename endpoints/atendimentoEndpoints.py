from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy import func
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
    #local_id = current_user["local_id"]
    #if not local_id:
    #    raise HTTPException(status_code=403, detail="Local não encontrado no token ou na requisição.")
    try:
        db_atendimento = Atendimento(**atendimento.dict())
        db_atendimento.data_registro = datetime.today()
        db_atendimento.user_id = current_user["id"]
    #    db_atendimento.local_id = current_user["local_id"]

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


@atendimento.put("/editar-atendimento/{atendimento_id}", response_model=AtendimentnoResponse)
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




@atendimento.get("/atendimento-count/{local_id}")
def count_atendimentos(
    local_id: int,
    periodo: str = Query("dia", enum=["dia", "semana", "mes", "ano"]),
    db: Session = Depends(get_db)

):

    campo_data = Atendimento.data

    if periodo == "dia":
        trunc = func.date_trunc('day', campo_data)
    elif periodo == "semana":
        trunc = func.date_trunc('week', campo_data)
    elif periodo == "mes":
        trunc = func.date_trunc('month', campo_data)
    else:
        trunc = func.date_trunc('year', campo_data)

    query = (
        db.query(
            trunc.label("periodo"),
            func.count(Atendimento.id).label("total")
        )
        .filter(Atendimento.local_id == local_id)
        .filter(campo_data.isnot(None))    
        .group_by(trunc)
        .order_by(trunc)
    )

    resultados = query.all()

    return [
        {
            "periodo": r.periodo.strftime("%Y-%m-%d"),
            "total_atendimentos": r.total
        }
        for r in resultados
    ]
