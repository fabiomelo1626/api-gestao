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
from schemas.tarefasSchema import TarefaResponse
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




#CONTAGEM DOS METAS
@dashboard.get("/metas-count", response_model=List[MetaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Metas).count()

#todas as metas atrasadas
@dashboard.get("/metas-atrasadas", response_model=List[MetaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Metas).filter(Metas.status == "Em atraso").all()

#quantidade de metas atrasadas
@dashboard.get("/metas-atrasadas-count", response_model=List[MetaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Metas).filter(Metas.status == "Em atraso").count()


#todos as concluidas
@dashboard.get("/metas-concluidas", response_model=List[MetaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Metas).filter(Metas.status == "Concluída").all()

#quantidade metas de concluidas
@dashboard.get("/metas-concluidos-count", response_model=List[MetaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Metas).filter(Metas.status == "Em atraso").count()

#todos as metas em andamenta
@dashboard.get("/metas-em-andamento", response_model=List[MetaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Metas).filter(Metas.status == "Em andamento").all()

#quantidade de metas em andamenta
@dashboard.get("/metas-em-andamento-count", response_model=List[MetaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Metas).filter(Metas.status == "Em andamento").count()




#CONTAGEM DOS TAREFAS
@dashboard.get("/tarefas-count", response_model=List[TarefaResponse])
def tarefas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Tarefa).count()

#todos as atrasadas
@dashboard.get("/tarefas-atrasadas", response_model=List[TarefaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Tarefa).filter(Tarefa.status == "Em atraso").all()

#quantidade de atrasadas
@dashboard.get("/tarefas-atrasadas-count", response_model=List[TarefaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Tarefa).filter(Tarefa.status == "Em atraso").count()


#todos os concluidas
@dashboard.get("/tarefas-concluidas", response_model=List[TarefaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Tarefa).filter(Tarefa.status == "Concluída").all()

#quantidade de concluidas
@dashboard.get("/tarefas-concluidos-count", response_model=List[TarefaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Tarefa).filter(Tarefa.status == "Em atraso").count()

#todos os em andamenta
@dashboard.get("/tarefas-em-andamento", response_model=List[TarefaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Tarefa).filter(Tarefa.status == "Em andamento").all()

#quantidade de em andamenta
@dashboard.get("/tarefas-em-andamento-count", response_model=List[TarefaResponse])
def metas_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Tarefa).filter(Tarefa.status == "Em andamento").count()


