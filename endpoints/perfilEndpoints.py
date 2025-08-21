from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.perfilModels import Perfil
from schemas.perfilSchema import PerfilCreate, PerfilResponse
from typing import List
from sqlalchemy import or_, desc, asc, String


perfil = APIRouter(prefix="/api")


@perfil.post("/create-perfil/", response_model=PerfilResponse)
def create_perfil(
    perfil: PerfilCreate,
    db: Session = Depends(get_db),
   
):
    existing_perfil = db.query(Perfil).filter(Perfil.descricao == perfil.descricao).first()
    if existing_perfil:
        raise HTTPException(status_code=400, detail="Perfil já cadastrado.")


    try:
        db_perfil = Perfil(**perfil.dict())
        db.add(db_perfil)
        db.commit()
        db.refresh(db_perfil)
        return db_perfil

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@perfil.get("/buscar-perfil/{perfil_id}", response_model=PerfilResponse)
def search_perfil(
    perfil_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    perfil = db.query(Perfil).filter(Perfil.id == perfil_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    return perfil


@perfil.get("/perfis", response_model=List[PerfilResponse])
def list_perfil(
    db: Session = Depends(get_db),
    #current_user: dict = Depends(get_current_user)
):
    perfil = db.query(Perfil).all()
    return perfil


@perfil.put("/editar-perfil/{perfil_id}", response_model=PerfilResponse)
def update_perfil(
    perfil_id: int,
    perfil: PerfilCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_perfil = db.query(Perfil).filter(Perfil.id == perfil_id).first()

    for key, value in perfil.dict().items():
        setattr(db_perfil, key, value)
    db.commit()
    db.refresh(db_perfil)

    return db_perfil
