from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.nascidoVivoModels import NascidoVivo
from schemas.nascidoVivoSchema import NascidoVivoCreate, NascidoVivoResponse
from sqlalchemy.exc import SQLAlchemyError

nascido_vivo = APIRouter(prefix="/api")


@nascido_vivo.post("/create-nascido-vivo/", response_model=NascidoVivoResponse)
def create_nascido_vivo(
    nascido: NascidoVivoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_nascido = NascidoVivo(**nascido.dict())
        db_nascido.data_registro = datetime.today()
        db_nascido.user_id = current_user["id"]
        # db_nascido.local_id = current_user.get("acesso_id")  # garantir que o acesso_id existe
        db.add(db_nascido)
        db.commit()
        db.refresh(db_nascido)
        return db_nascido

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@nascido_vivo.get("/busca-nascido-vivo/{nascido_id}", response_model=NascidoVivoResponse)
def search_nascido_vivo(nascido_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    nascido = db.query(NascidoVivo).filter(NascidoVivo.id == nascido_id).first()
    if not nascido:
        raise HTTPException(status_code=404, detail="Nascido vivo não encontrado")
    return nascido


@nascido_vivo.get("/nascidos-vivos", response_model=List[NascidoVivoResponse])
def nascidos_vivos_all(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    nascidos = db.query(NascidoVivo).all()
    return nascidos


@nascido_vivo.get("/nascidos-by-local_id/{local_id}", response_model=List[NascidoVivoResponse])
def search_nascido_vivo_local(local_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    nascidos = db.query(NascidoVivo).filter(NascidoVivo.local_id == local_id).all()
   
    return nascidos


@nascido_vivo.put("/editar-nascido-vivo/{nascido_id}", response_model=NascidoVivoResponse)
def update_nascido_vivo(
    nascido_id: int,
    nascido: NascidoVivoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_nascido = db.query(NascidoVivo).filter(NascidoVivo.id == nascido_id).first()
    if not db_nascido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nascido vivo não encontrado")

    try:
        # Atualiza apenas os campos enviados
        for key, value in nascido.dict(exclude_unset=True).items():
            setattr(db_nascido, key, value)

        db_nascido.data_alteracao = datetime.today()
        db_nascido.user_id = current_user["id"]
        db.commit()
        db.refresh(db_nascido)
        return db_nascido

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
