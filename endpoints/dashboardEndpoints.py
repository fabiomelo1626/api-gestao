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