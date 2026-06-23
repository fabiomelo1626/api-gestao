from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.metasModels import Metas
from schemas.metasSchema import *
from utils.middlewareDependence import check_permission


metas = APIRouter(prefix="/api")



@metas.post("/create-meta/", response_model=MetaResponse)
def create_meta(
    meta: MetaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    dependencies=[Depends(check_permission("tabela_setor", "criar"))]
):
   
    try:
        db_meta = Metas(**meta.dict())
        db_meta.data_registro = datetime.today()
        db_meta.user_id = current_user["id"]
        db_meta.local_id = meta.local_id

        db.add(db_meta)
        db.commit()
        db.refresh(db_meta)
        return db_meta

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@metas.get("/busca-meta/{meta_id}", response_model=MetaResponse)
def search_meta(
    meta_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    dependencies=[Depends(check_permission("tabela_setor", "listar"))]
):
    db_meta = db.query(Metas).filter(Metas.id == meta_id).first()
    if not db_meta:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    return db_meta


@metas.get("/meats", response_model=List[MetaResponse])
def mestas_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    dependencies=[Depends(check_permission("tabela_setor", "listar"))]
):
    return db.query(Metas).all()


@metas.get("/metas-by-local_id/{local_id}", response_model=List[MetaResponse])
def search_metas_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    dependencies=[Depends(check_permission("tabela_setor", "listar"))]
):
    metas = db.query(Metas).filter(Metas.local_id == local_id).all()
   
    return metas


@metas.put("/editar-meta/{meta_id}", response_model=MetaResponse)
def update_meta(
    meta_id: int,
    meta: MetaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    dependencies=[Depends(check_permission("tabela_setor", "editar"))]
):
    db_meta = db.query(Metas).filter(Metas.id == meta_id).first()
    if not db_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta não encontrada")

    try:
        for key, value in meta.dict(exclude_unset=True).items():
            setattr(db_meta, key, value)

        db_meta.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_meta)
        return db_meta

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
