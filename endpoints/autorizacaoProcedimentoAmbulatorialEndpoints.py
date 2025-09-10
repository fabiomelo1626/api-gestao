from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.autorizacaoProcedimentoAmbulatorialModels import AutorizacaoProcedimentoAmbulatorial
from schemas.autorizacaoProcedimentoAmbulatorialSchema import AutorizacaoProcedimentoAmbulatorialCreate, AutorizacaoProcedimentoAmbulatorialResponse

autorizacao = APIRouter(prefix="/api")


@autorizacao.post("/create-autorizacao-leito/", response_model=AutorizacaoProcedimentoAmbulatorialResponse)
def create_autorizacao(
    autorizacao: AutorizacaoProcedimentoAmbulatorialCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_autorizacao = AutorizacaoProcedimentoAmbulatorial(**autorizacao.dict())
        db_autorizacao.data_registro = datetime.today()
        db_autorizacao.user_id = current_user["id"]
        # db_autorizacao.local_id = current_user["acesso_id"]
        db.add(db_autorizacao)
        db.commit()
        db.refresh(db_autorizacao)
        return db_autorizacao
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@autorizacao.get("/busca-autorizacao/{autorizacao_id}", response_model=AutorizacaoProcedimentoAmbulatorialResponse)
def search_autorizacao(autorizacao_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_autorizacao = db.query(AutorizacaoProcedimentoAmbulatorial).filter(
        AutorizacaoProcedimentoAmbulatorial.id == autorizacao_id
    ).first()
    if not db_autorizacao:
        raise HTTPException(status_code=404, detail="Autorização Procedimento não encontrada")
    return db_autorizacao


@autorizacao.get("/autorizacoes-procedimentos", response_model=List[AutorizacaoProcedimentoAmbulatorialResponse])
def autorizacoes_all(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(AutorizacaoProcedimentoAmbulatorial).all()


@autorizacao.get("/autorizacoes-by-local_id/{local_id}", response_model=List[AutorizacaoProcedimentoAmbulatorialResponse])
def search_autorizacao_procedimento_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    autorizacoes = db.query(AutorizacaoProcedimentoAmbulatorial).filter(
        AutorizacaoProcedimentoAmbulatorial.local_id == local_id
    ).all()
    if not autorizacoes:
        raise HTTPException(status_code=404, detail="Nenhuma autorização encontrada para o local")
    return autorizacoes


@autorizacao.put("/editar-autorizacao-procedimento/{autorizacao_id}", response_model=AutorizacaoProcedimentoAmbulatorialResponse)
def update_autorizacao(
    autorizacao_id: int,
    autorizacao_in: AutorizacaoProcedimentoAmbulatorialCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_autorizacao = db.query(AutorizacaoProcedimentoAmbulatorial).filter(
        AutorizacaoProcedimentoAmbulatorial.id == autorizacao_id
    ).first()
    if not db_autorizacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autorização Procedimento não encontrada")

    try:
        # Atualiza somente os campos enviados
        for key, value in autorizacao_in.dict(exclude_unset=True).items():
            setattr(db_autorizacao, key, value)

        db_autorizacao.data_alteracao = datetime.today()
        db.commit()
        db.refresh(db_autorizacao)
        return db_autorizacao

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
