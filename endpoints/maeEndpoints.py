from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.maeModels import Mae
from schemas.maeSchema import MaeCreate, MaeResponse

mae = APIRouter(prefix="/api")


@mae.post("/create-mae/", response_model=MaeResponse)
def create_mae(
    mae_in: MaeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_mae = Mae(**mae_in.dict())
        db_mae.data_registro = datetime.today()
        db_mae.user_id = current_user["id"]
        # db_mae.local_id = current_user.get("acesso_id")
        db.add(db_mae)
        db.commit()
        db.refresh(db_mae)
        return db_mae

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@mae.get("/busca-mae/{mae_id}", response_model=MaeResponse)
def search_mae(mae_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    mae_obj = db.query(Mae).filter(Mae.id == mae_id).first()
    if not mae_obj:
        raise HTTPException(status_code=404, detail="Mãe não encontrada")
    return mae_obj


@mae.get("/maes", response_model=List[MaeResponse])
def mae_all(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    maes = db.query(Mae).all()
    return maes


@mae.get("/maes-by-local_id/{local_id}", response_model=List[MaeResponse])
def search_mae_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    maes = db.query(Mae).filter(Mae.local_id == local_id).all()
    
    return maes


@mae.put("/editar-mae/{mae_id}", response_model=MaeResponse)
def update_mae(
    mae_id: int,
    mae_in: MaeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_mae = db.query(Mae).filter(Mae.id == mae_id).first()
    if not db_mae:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mãe não encontrada")

    try:
        # Atualiza apenas os campos enviados
        for key, value in mae_in.dict(exclude_unset=True).items():
            setattr(db_mae, key, value)

        db_mae.data_alteracao = datetime.today()
        db_mae.user_id = current_user["id"]
        db.commit()
        db.refresh(db_mae)
        return db_mae

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
