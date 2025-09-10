from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.estabelecimentoLeitoModels import EstabelecimentoLeito
from schemas.estabelecimentoLeitoSchema import (
    EstabelecimentoLeitoCreate,
    EstabelecimentoLeitoResponse
)
from sqlalchemy.exc import SQLAlchemyError

estabelecimento_leito = APIRouter(prefix="/api")


# Criar estabelecimento leito
@estabelecimento_leito.post("/create-estabelecimento-leito/", response_model=EstabelecimentoLeitoResponse)
def create_estabelecimento(
    estabelecimento_data: EstabelecimentoLeitoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_estabelecimento = EstabelecimentoLeito(**estabelecimento_data.dict())
        db_estabelecimento.data_registro = datetime.today()
        db_estabelecimento.user_id = current_user["id"]
        db_estabelecimento.acesso_id = current_user.get("acesso_id")

        db.add(db_estabelecimento)
        db.commit()
        db.refresh(db_estabelecimento)
        return db_estabelecimento

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


# Buscar estabelecimento leito por ID
@estabelecimento_leito.get("/busca-estabelecimento_leito/{estabelecimento_leito_id}", response_model=EstabelecimentoLeitoResponse)
def search_estabelecimento(estabelecimento_leito_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimento = db.query(EstabelecimentoLeito).filter(EstabelecimentoLeito.id == estabelecimento_leito_id).first()
    if not estabelecimento:
        raise HTTPException(status_code=404, detail="Estabelecimento leito não encontrado")
    return estabelecimento


# Listar todos os estabelecimentos leitos
@estabelecimento_leito.get("/estabelecimento_leitos", response_model=List[EstabelecimentoLeitoResponse])
def estabelecimento_leitos_all(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(EstabelecimentoLeito).all()


# Buscar estabelecimentos leitos por local_id
@estabelecimento_leito.get("/estabelecimento_leito-by-local_id/{local_id}", response_model=List[EstabelecimentoLeitoResponse])
def search_estabelecimento_leito_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimentos = db.query(EstabelecimentoLeito).filter(EstabelecimentoLeito.local_id == local_id).all()
    if not estabelecimentos:
        raise HTTPException(status_code=404, detail="Nenhum estabelecimento leito encontrado para o local")
    return estabelecimentos


# Editar estabelecimento leito
@estabelecimento_leito.put("/editar-estabelecimento_leito/{estabelecimento_leito_id}", response_model=EstabelecimentoLeitoResponse)
def update_estabelecimento_leito(
    estabelecimento_leito_id: int,
    estabelecimento_data: EstabelecimentoLeitoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_estabelecimento = db.query(EstabelecimentoLeito).filter(EstabelecimentoLeito.id == estabelecimento_leito_id).first()
    if not db_estabelecimento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estabelecimento leito não encontrado")

    try:
        for key, value in estabelecimento_data.dict(exclude_unset=True).items():
            setattr(db_estabelecimento, key, value)

        db_estabelecimento.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_estabelecimento)
        return db_estabelecimento

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
