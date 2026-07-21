from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.projetosModels import Projeto
from schemas.projetosShema import *
from utils.middlewareDependence import check_permission


projetos = APIRouter(prefix="/api")



@projetos.post("/create-projeto/", 
               response_model=ProjetoResponse, 
               dependencies=[Depends(check_permission("tabela_projetos", "criar"))]
               )
def create_projeto(
    projeto: ProjetoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
   
    try:
        db_projeto = Projeto(**projeto.dict())
        db_projeto.data_registro = datetime.today()
        db_projeto.user_id = current_user["id"]
        db_projeto.local_id = projeto.local_id

        db.add(db_projeto)
        db.commit()
        db.refresh(db_projeto)
        return db_projeto

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@projetos.get("/busca-projeto/{projeto_id}", 
              response_model=ProjetoResponse, 
              dependencies=[Depends(check_permission("tabela_projetos", "listar"))]
              )
def search_projeto(
    projeto_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    db_projeto = db.query(Projeto).filter(Projeto.id == projeto_id).first()
    if not db_projeto:
        raise HTTPException(status_code=404, detail="projeto não encontrado")
    return db_projeto


@projetos.get("/projetos", 
              response_model=List[ProjetoResponse], 
              dependencies=[Depends(check_permission("tabela_projetos", "listar"))]
              )
def projetos_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).all()




#CONTAGEM DOS PROJETOS
@projetos.get("/projetos-count", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).count()

#todos os atrasados
@projetos.get("/projetos-atrasados", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).filter(Projeto.status == "Em atraso").all()

#quantidade de atrasados
@projetos.get("/projetos-atrasados-count", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).filter(Projeto.status == "Em atraso").count()



#todos os concluidos
@projetos.get("/projetos-concluidos", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).filter(Projeto.status == "Concluída").all()

#quantidade de concluidos
@projetos.get("/projetos-atrasados-count", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).filter(Projeto.status == "Concluída").count()


#todos os em andamento
@projetos.get("/projetos-em-andamento", 
              response_model=List[ProjetoResponse], 
              dependencies=[Depends(check_permission("tabela_projetos", "listar"))]
              )
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),

    
):
    return db.query(Projeto).filter(Projeto.status == "Em andamento").all()

#quantidade de em andamento
@projetos.get("/projetos-em-andamento-count", response_model=List[ProjetoResponse])
def projetos_count_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    return db.query(Projeto).filter(Projeto.status == "Em andamento").count()




@projetos.get("/projetos-by-local_id/{local_id}", 
              response_model=List[ProjetoResponse], 
              dependencies=[Depends(check_permission("tabela_projetos", "listar"))]
              )
def search_projetos_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    projetos = db.query(Projeto).filter(Projeto.local_id == local_id).all()
   
    return projetos


@projetos.put("/editar-projeto/{projeto_id}", 
              response_model=ProjetoResponse, 
              dependencies=[Depends(check_permission("tabela_projetos", "editar"))]
              )
def update_projeto(
    projeto_id: int,
    projeto: ProjetoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_projeto = db.query(Projeto).filter(Projeto.id == projeto_id).first()
    if not db_projeto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="projeto não encontrado")

    try:
        for key, value in projeto.dict(exclude_unset=True).items():
            setattr(db_projeto, key, value)

        db_projeto.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_projeto)
        return db_projeto

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
