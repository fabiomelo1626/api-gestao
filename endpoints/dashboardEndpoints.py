from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.metasModels import Metas
from models.pessoaModels import Pessoa
from models.projetosModels import Projeto
from models.tarefasModels import Tarefa
from schemas.metasSchema import *
from schemas.projetosShema import ProjetoResponse
from utils.middlewareDependence import check_permission


dashboard = APIRouter(prefix="/api")

@dashboard.get("/dashboard/status")
def get_status_all(db: Session = Depends(get_db)): 
    return{
        "total_pessoas": db.query(Pessoa).count(),
        "total_projetos": db.query(Projeto).count(),
        "total_metas": db.query(Metas).count(),
        "total_tarefas": db.query(Tarefa).count()
    }

@dashboard.get("/dashboard/projetos/destaque/{local_id}")
def get_projetos_destaque_all(local_id: int, db: Session = Depends(get_db)): 
    return db.query(Projeto).filter(Projeto.local_id==local_id).order_by(Projeto.id.desc()).limit(3).all()
        

@dashboard.get("/dashboard/tarefas/destaque/{local_id}")
def get_tarefas_destaque_all(local_id: int, db: Session = Depends(get_db)): 
    atividades =  db.query(Tarefa).filter(Tarefa.local_id==local_id).order_by(Tarefa.data_alteracao.desc()).limit(5).all()

    return atividades





#CONTAGEM DOS PROJETOS
@dashboard.get("/projetos-count", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).count()

#todos os atrasados
@dashboard.get("/projetos-atrasados", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).filter(Projeto.status == "Em atraso").all()

#quantidade de atrasados
@dashboard.get("/projetos-atrasados-count", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).filter(Projeto.status == "Em atraso").count()



#todos os concluidos
@dashboard.get("/projetos-concluidos", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).filter(Projeto.status == "Concluída").all()

#quantidade de concluidos
@dashboard.get("/projetos-atrasados-count", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).filter(Projeto.status == "Concluída").count()


#todos os em andamento
@dashboard.get("/projetos-em-andamento", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).filter(Projeto.status == "Em andamento").all()

#quantidade de em andamento
@dashboard.get("/projetos-em-andamento-count", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).filter(Projeto.status == "Em andamento").count()


