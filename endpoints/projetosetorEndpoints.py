from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.projetoSetorModels import ProjetoSetor
from schemas.cargoSchema import *
from schemas.projetoSetorSchema import ProjetoSetorCreate, ProjetoSetorResponse
from utils.middlewareDependence import check_permission


projeto_setor = APIRouter(prefix="/api")


@projeto_setor.post("/create-projeto-setor/", 
            response_model=ProjetoSetorResponse, 
            dependencies=[Depends(check_permission("tabela_projeto_setor", "criar"))]
            )
def create_projeto_setor(
    projeto: ProjetoSetorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    
    try:
        db_projeto_setor = ProjetoSetor(**projeto.dict())
        db_projeto_setor.data_registro = datetime.today()
        db_projeto_setor.user_id = current_user["id"]
        db_projeto_setor.local_id = projeto.local_id

        db.add(db_projeto_setor)
        db.commit()
        db.refresh(db_projeto_setor)
        return db_projeto_setor

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@projeto_setor.get("/busca-projeto-setor/{projeto_setor_id}", 
           response_model=ProjetoSetorResponse, 
           dependencies=[Depends(check_permission("tabela_projeto_setor", "listar"))]
           )
def search_projeto_setor(
    projeto_setor_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_projeto_setor = db.query(ProjetoSetor).filter(ProjetoSetor.id == projeto_setor_id).first()
    if not db_projeto_setor:
        raise HTTPException(status_code=404, detail="projeto setor não encontrado")
    return db_projeto_setor



@projeto_setor.get("/projeto-setor", 
           response_model=List[ProjetoSetorResponse], 
           dependencies=[Depends(check_permission("tabela_cargos", "listar"))]
           )
def projeto_setor_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    ):
    return db.query(ProjetoSetor).all()



@projeto_setor.get("/projeto-setor-by-local_id/{local_id}", 
           response_model=List[ProjetoSetorResponse], 
           dependencies=[Depends(check_permission("tabela_projeto_setor", "listar"))]
           )
def search_projeto_setor_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    projeto_setor = db.query(ProjetoSetor).filter(ProjetoSetor.local_id == local_id).all()
   
    return projeto_setor



@projeto_setor.put("/editar-projeto-setor/{projeto_setor_id}", 
           response_model=ProjetoSetorResponse, 
           dependencies=[Depends(check_permission("tabela_projeto_setor", "editar"))]
           )
def update_cargo(
    projeto_setor_id: int,
    projeto_setor: ProjetoSetorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_projeto_Setor = db.query(ProjetoSetor).filter(ProjetoSetor.id == projeto_setor_id).first()
    if not db_projeto_Setor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="projeto setor não encontrado")

    try:
        for key, value in projeto_setor.dict(exclude_unset=True).items():
            setattr(db_projeto_Setor, key, value)

        db_projeto_Setor.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_projeto_Setor)
        return db_projeto_Setor

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
