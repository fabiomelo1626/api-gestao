from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.cargoModels import Cargo
from schemas.cargoSchema import *
from utils.middlewareDependence import check_permission


cargo = APIRouter(prefix="/api")



@cargo.post("/create-cargo/", response_model=CargoResponse)
def create_cargo(
    cargo: CargoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    dependencies=[Depends(check_permission("tabela_setor", "criar"))]
):
    
    try:
        db_cargo = Cargo(**cargo.dict())
        db_cargo.data_registro = datetime.today()
        db_cargo.user_id = current_user["id"]
        db_cargo.local_id = cargo.local_id

        db.add(db_cargo)
        db.commit()
        db.refresh(db_cargo)
        return db_cargo

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@cargo.get("/busca-cargo/{cargo_id}", response_model=CargoResponse)
def search_cargo(
    cargo_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    dependencies=[Depends(check_permission("tabela_setor", "listar"))]
):
    db_cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not db_cargo:
        raise HTTPException(status_code=404, detail="cargo não encontrado")
    return db_cargo



@cargo.get("/cargos", response_model=List[CargoResponse])
def cargos_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    dependencies=[Depends(check_permission("tabela_setor", "listar"))]
    ):
    return db.query(Cargo).all()



@cargo.get("/cargos-by-local_id/{local_id}", response_model=List[CargoResponse])
def search_cargos_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    dependencies=[Depends(check_permission("tabela_setor", "listar"))]
):
    cargos = db.query(Cargo).filter(Cargo.local_id == local_id).all()
   
    return cargos



@cargo.put("/editar-cargo/{cargo_id}", response_model=CargoResponse)
def update_cargo(
    cargo_id: int,
    cargo: CargoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    dependencies=[Depends(check_permission("tabela_setor", "editar"))]
):
    db_cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not db_cargo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cargo não encontrado")

    try:
        for key, value in cargo.dict(exclude_unset=True).items():
            setattr(db_cargo, key, value)

        db_cargo.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_cargo)
        return db_cargo

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
