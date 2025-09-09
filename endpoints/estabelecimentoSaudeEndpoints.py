from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.acessoModels import Acesso
from models.estabelecimentoSaudeModels import EstabelecimentoSaude
from schemas.estabelecimentoSaudeSchema import EstabelecimentoSaudeCreate, EstabelecimentoSaudeResponse, EstabelecimentoSaudeUpdate

estabelecimento = APIRouter(prefix="/api")


@estabelecimento.post("/create-estabelecimento-saude/", response_model=EstabelecimentoSaudeResponse)
def create_estabelecimento(
    estabelecimento: EstabelecimentoSaudeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_estabelecimento = EstabelecimentoSaude(**estabelecimento.dict())
        db_estabelecimento.data_registro = datetime.today()
        db_estabelecimento.user_id = current_user["id"]
        # db_estabelecimento.local_id = current_user["local_id"]
        db.add(db_estabelecimento)
        db.commit()
        db.refresh(db_estabelecimento)
        return db_estabelecimento
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@estabelecimento.put("/editar-estabelecimento-saude/{estabelecimento_id}", response_model=EstabelecimentoSaudeResponse)
def update_estabelecimento(
    estabelecimento_id: int,
    estabelecimento: EstabelecimentoSaudeUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_estabelecimento = db.query(EstabelecimentoSaude).filter(EstabelecimentoSaude.id == estabelecimento_id).first()
    if not db_estabelecimento:
        raise HTTPException(status_code=404, detail="Estabelecimento não encontrado")
    
    try:
        # Atualiza campos fornecidos
        for key, value in estabelecimento.dict().items():
            setattr(db_estabelecimento, key, value)
        db_estabelecimento.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_estabelecimento)
        return db_estabelecimento
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@estabelecimento.get("/busca-estabelecimento-saude/{estabelecimento_id}", response_model=EstabelecimentoSaudeResponse)
def search_estabelecimento(estabelecimento_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estabelecimento = db.query(EstabelecimentoSaude).filter(EstabelecimentoSaude.id == estabelecimento_id).first()
    if not estabelecimento:
        raise HTTPException(status_code=404, detail="Estabelecimento não encontrado")
    return estabelecimento


@estabelecimento.get("/estabelecimentos-saude", response_model=List[EstabelecimentoSaudeResponse])
def get_estabelecimentos(
    local_id: Optional[int] = Query(None),
    nome: Optional[str] = Query(None),
    ordenar_por: Optional[str] = Query(None),
    ordem: str = Query("asc"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(EstabelecimentoSaude)

    # Filtros opcionais
    if local_id:
        query = query.filter(EstabelecimentoSaude.local_id == local_id)
    if nome:
        query = query.filter(func.lower(EstabelecimentoSaude.nome) == nome.lower())

    # Ordenação
    if ordenar_por and hasattr(EstabelecimentoSaude, ordenar_por):
        coluna = getattr(EstabelecimentoSaude, ordenar_por)
        query = query.order_by(desc(coluna) if ordem == "desc" else asc(coluna))

    return query.all()


@estabelecimento.get("/estabelecimentos-saude-by-local_id/{local_id}", response_model=List[EstabelecimentoSaudeResponse])
def search_estabelecimento_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    acesso = db.query(Acesso).filter(
        Acesso.id == local_id,
        Acesso.usuario_id == current_user["id"],
        Acesso.ativo == True
    ).first()
    
    if not acesso:
        raise HTTPException(
            status_code=403,
            detail="Acesso não encontrado ou você não tem permissão."
        )

    localacesso_id = acesso.localacesso_id

    estabelecimento = db.query(EstabelecimentoSaude).filter(
        EstabelecimentoSaude.local_id == localacesso_id
    ).all()

    return estabelecimento
