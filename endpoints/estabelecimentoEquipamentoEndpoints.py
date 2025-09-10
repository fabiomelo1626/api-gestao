from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.estabelecimentoEquipamentoModels import EstabelecimentoEquipamento
from schemas.estabelecimentoEquipamentoSchema import (
    EstabelecimentoEquipamentoCreate,
    EstabelecimentoEquipamentoResponse
)
from sqlalchemy.exc import SQLAlchemyError

estabelecimento_equipamento = APIRouter(prefix="/api")


# Criar estabelecimento equipamento
@estabelecimento_equipamento.post("/create-estabelecimento/", response_model=EstabelecimentoEquipamentoResponse)
def create_estabelecimento(
    estabelecimento: EstabelecimentoEquipamentoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_equipamento = EstabelecimentoEquipamento(**estabelecimento.dict())
        db_equipamento.data_registro = datetime.today()
        db_equipamento.user_id = current_user["id"]
        # db_equipamento.local_id = current_user.get("acesso_id")

        db.add(db_equipamento)
        db.commit()
        db.refresh(db_equipamento)
        return db_equipamento

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


# Buscar estabelecimento equipamento por ID
@estabelecimento_equipamento.get("/busca-estabelecimento/{estabelecimento_id}", response_model=EstabelecimentoEquipamentoResponse)
def search_estabelecimento(estabelecimento_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    equipamento = db.query(EstabelecimentoEquipamento).filter(EstabelecimentoEquipamento.id == estabelecimento_id).first()
    if not equipamento:
        raise HTTPException(status_code=404, detail="Estabelecimento equipamento não encontrado")
    return equipamento


# Listar todos os estabelecimentos equipamentos
@estabelecimento_equipamento.get("/estabelecimentos", response_model=List[EstabelecimentoEquipamentoResponse])
def vinculo_all(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(EstabelecimentoEquipamento).all()


# Buscar estabelecimentos equipamentos por local_id
@estabelecimento_equipamento.get("/estabelecimentos-by-local_id/{local_id}", response_model=List[EstabelecimentoEquipamentoResponse])
def search_estabelecimento_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    equipamentos = db.query(EstabelecimentoEquipamento).filter(EstabelecimentoEquipamento.local_id == local_id).all()
    return equipamentos


# Editar estabelecimento equipamento
@estabelecimento_equipamento.put("/editar-estabelecimento/{estabelecimento_id}", response_model=EstabelecimentoEquipamentoResponse)
def update_estabelecimento(
    estabelecimento_id: int,
    vinculo: EstabelecimentoEquipamentoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_equipamento = db.query(EstabelecimentoEquipamento).filter(EstabelecimentoEquipamento.id == estabelecimento_id).first()
    if not db_equipamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estabelecimento não encontrado")

    try:
        for key, value in vinculo.dict(exclude_unset=True).items():
            setattr(db_equipamento, key, value)

        db_equipamento.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_equipamento)
        return db_equipamento

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
