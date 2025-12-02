from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.tabelasAuxiliaresModels import Setor
from schemas.setorSchema import SetorCreate, SetorResponse
from utils.middlewareDependence import check_permission


setor = APIRouter(prefix="/api")



@setor.post("/create-setor/", response_model=SetorResponse)
def create_setor(
    setor: SetorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    local_id = setor.local_id
    if not local_id:
       raise HTTPException(status_code=403, detail="Local não encontrado no token ou na requisição.")
    
    try:
        db_setor = Setor(**setor.dict())
        db_setor.data_registro = datetime.today()
        db_setor.user_id = current_user["id"]
    #    db_setor.local_id = current_user['local_id']

        db.add(db_setor)
        db.commit()
        db.refresh(db_setor)
        return db_setor

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@setor.get("/busca-setor/{setor_id}", response_model=SetorResponse)
def search_setor(
    setor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_setor = db.query(Setor).filter(Setor.id == setor_id).first()
    if not db_setor:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    return db_setor


@setor.get(
    "/setores",
    dependencies=[Depends(check_permission("setor", "listar"))],
    response_model=List[SetorResponse]
)
def setores_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Setor).all()


@setor.get("/setores-by-local_id/{local_id}", response_model=List[SetorResponse])
def search_setores_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    setores = db.query(Setor).filter(Setor.local_id == local_id).all()
   
    return setores


@setor.put("/editar-setor/{setor_id}", response_model=SetorResponse)
def update_pessoa(
    setor_id: int,
    setor: SetorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_setor = db.query(Setor).filter(Setor.id == setor_id).first()
    if not db_setor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setor não encontrado")

    try:
        for key, value in setor.dict(exclude_unset=True).items():
            setattr(db_setor, key, value)

        db_setor.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_setor)
        return db_setor

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
