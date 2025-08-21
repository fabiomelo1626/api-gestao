from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from sqlalchemy import or_, asc, desc

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.localAcessoModels import LocalAcesso
from schemas.localAcessoSchema import LocalAcessoCreate, LocalAcessoResponse
from models.acessoModels import Acesso 
local = APIRouter(prefix="/api")


@local.post("/create-local/", response_model=LocalAcessoResponse, status_code=status.HTTP_201_CREATED)
def create_local(local: LocalAcessoCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if db.query(LocalAcesso).filter(LocalAcesso.cnpj == local.cnpj).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Local com este CNPJ já cadastrado.")

    try:
        db_local = LocalAcesso(**local.dict())
        db.add(db_local)
        db.commit()
        db.refresh(db_local)
        return db_local
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")


@local.put("/editar-local/{local_id}", response_model=LocalAcessoResponse)
def update_local(local_id: int, local: LocalAcessoCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_local = db.query(LocalAcesso).filter(LocalAcesso.id == local_id).first()
    if not db_local:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Local não encontrado.")

    try:
        for key, value in local.dict().items():
            setattr(db_local, key, value)
        db.commit()
        db.refresh(db_local)
        return db_local
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")


@local.get("/buscar-local/{local_id}", response_model=LocalAcessoResponse)
def buscar_local(local_id: int, db: Session = Depends(get_db)):
    local = db.query(LocalAcesso).filter(LocalAcesso.id == local_id).first()
    if not local:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Local não encontrado")
    return local



@local.get("/locais", response_model=List[LocalAcessoResponse])
def listar_locais(
    nome: str = Query(None),
    cnpj: str = Query(None),
    Cidade: str = Query(None),
    Estado: str = Query(None),
    ordem: str = Query("asc"),
    db: Session = Depends(get_db),
):
    query = db.query(LocalAcesso)

    if nome:
        query = query.filter(LocalAcesso.nome == nome)
    if cnpj:
        query = query.filter(LocalAcesso.cnpj == cnpj)
    if Cidade:
        query = query.filter(LocalAcesso.Cidade == Cidade)
    if Estado:
        query = query.filter(LocalAcesso.Estado == Estado)

    if ordem and hasattr(LocalAcesso, ordem):
        if ordem == "desc":
            query = query.order_by(desc(getattr(LocalAcesso, ordem)))
        else:
            query = query.order_by(asc(getattr(LocalAcesso, ordem)))

    return query.all()
    

@local.delete("/inativar-local/{local_id}", response_model=LocalAcessoResponse)
def inativar_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_local = db.query(LocalAcesso).filter(LocalAcesso.id == local_id).first()
    if not db_local:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Local não encontrado")

    db_local.is_active = False
    db.commit()
    db.refresh(db_local)
    return db_local
