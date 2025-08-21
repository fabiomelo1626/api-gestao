from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.saudeMentalModels import SaudeMental
from schemas.saudeMentalSchema import SaudeMentalCreate, SaudeMentalResponse
from sqlalchemy import asc, desc, func
from sqlalchemy.exc import SQLAlchemyError


saude_mental = APIRouter(prefix="/api")



@saude_mental.post("/create-saude-mental/", response_model=SaudeMentalResponse)
def create_saude_mental(
    saude: SaudeMentalCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    try:
        db_saude = SaudeMental(**saude.dict())
        db_saude.data_registro = datetime.today()
        db.add(db_saude)
        db.commit()
        db.refresh(db_saude)
        return db_saude
   

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@saude_mental.get("/busca-saude-mental/{saude_id}", response_model=SaudeMentalResponse)
def search_saude_mental(saude_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    saude = db.query(SaudeMental).filter(SaudeMental.id == saude_id).first()
    if not saude:
        raise HTTPException(status_code=404, detail="Saude Mental não encontrada")
    return saude



@saude_mental.get("/saudes-mentais", response_model=SaudeMentalResponse)
def saude_mental_all(db:Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    saudes = db.query(SaudeMental).all()

    return saudes



@saude_mental.get("/saude-mental-by-local_id/{local_id}", response_model=SaudeMentalResponse)
def search_saude_mental_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    saudes = db.query(SaudeMental).filter(SaudeMental.local_id == local_id).first()
    if not saudes:
        HTTPException(status_code=404, detail="Saude mental  não encontrada para o local")
    return saudes



@saude_mental.put("/editar-saude-mental/{saude_id}", response_model=SaudeMentalResponse)
def update_saude_mental(
    saude_id: int,
    saude: SaudeMentalCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_saude = db.query(SaudeMental).filter(SaudeMental.id == saude_id).first()

    if not db_saude:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saude Mental não encontrada")

    try:
        db_saude = SaudeMental(**saude.dict())
        db_saude.data_alteracao = datetime.today()
        db.add(db_saude)
        db.commit()
        db.refresh(db_saude)
        return db_saude
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
