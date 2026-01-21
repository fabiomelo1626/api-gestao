from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.tarefasModels import Tarefa
from schemas.tarefasSchema import *
from utils.middlewareDependence import check_permission


tarefas = APIRouter(prefix="/api")



@tarefas.post("/create-tarefa/", response_model=TarefaResponse)
def create_tarefa(
    tarefa: TarefaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    
    
    try:
        db_tarefa = Tarefa(**tarefa.dict())
        db_tarefa.data_registro = datetime.today()
        db_tarefa.user_id = current_user["id"]
        db_tarefa.local_id = db_tarefa.local_id

        db.add(db_tarefa)
        db.commit()
        db.refresh(db_tarefa)
        return db_tarefa

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@tarefas.get("/busca-tarefa/{tarefa_id}", response_model=TarefaResponse)
def search_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa


@tarefas.get("/tarefas", response_model=List[TarefaResponse])
def tarefas_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Tarefa).all()


@tarefas.get("/tarefas-by-local_id/{local_id}", response_model=List[TarefaResponse])
def search_tarefas_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tarefas = db.query(Tarefa).filter(Tarefa.local_id == local_id).all()
    for tarefa in tarefas:
        if (
            tarefa.data_conclusao
            and tarefa.data_conclusao < date.today()
            and tarefa.status != "Concluída"
        ):
            tarefa.status = "Em atraso"

    db.commit()
   
    return tarefas



@tarefas.put("/novo-prazo-tarefa/{tarefa_id}", response_model=TarefaResponse)
def novo_prazo_tarefa(
    tarefa_id: int,
      nova_data : datetime,
        db: Session = Depends(get_db),
          current_user: dict = Depends(get_current_user)
          ):
        db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
        if not db_tarefa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
        try:
            db_tarefa.data_conclusao = nova_data
            db.commit()
            db.refresh(db_tarefa)
            return db_tarefa
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")




@tarefas.put("/editar-tarefa/{tarefa_id}", response_model=TarefaResponse)
def update_tarefa(
    tarefa_id: int,
    tarefa: TarefaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not db_tarefa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")

    try:
        for key, value in tarefa.dict(exclude_unset=True).items():
            setattr(db_tarefa, key, value)

        db_tarefa.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_tarefa)
        return db_tarefa

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
