from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.metasModels import Metas
from models.projetoSetorModels import ProjetoSetor
from models.projetosModels import Projeto
from schemas.projetosSchema import *
from utils.middlewareDependence import check_permission
import logging
import traceback


logger = logging.getLogger(__name__)

projetos = APIRouter(prefix="/api")



@projetos.post(
    "/create-projeto/", 
    response_model=ProjetoResponse, 
    dependencies=[Depends(check_permission("tabela_projetos", "criar"))]
)
def create_projeto(
    projeto: ProjetoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        dados_projeto = projeto.dict()

        # Extrai os IDs e remove TODAS as variações de chaves de setores
        setores_ids = (
            dados_projeto.pop("setores_ids", None) 
            or dados_projeto.pop("setor_id", None) 
            or []
        )
        
        # Garante que seja uma lista (caso tenha vindo apenas um inteiro)
        if isinstance(setores_ids, int):
            setores_ids = [setores_ids]

        # Remove qualquer relacionamento com nome similar que possa estar no dict
        dados_projeto.pop("setores", None)
        dados_projeto.pop("projetos_setores", None)

        # 1. Instancia o Projeto (agora totalmente limpo de qualquer chave 'setor')
        db_projeto = Projeto(**dados_projeto)
        db_projeto.data_registro = datetime.today()
        db_projeto.user_id = current_user["id"]
        db_projeto.local_id = projeto.local_id

        db.add(db_projeto)
        db.flush()  

        # 2. Cria os vínculos na tabela intermediária
        for s_id in setores_ids:
            vinculo = ProjetoSetor(
                projeto_id=db_projeto.id,
                setor_id=s_id,
                user_id=current_user["id"],
                local_id=projeto.local_id,
                data_registro=datetime.today()
            )
            db.add(vinculo)

        db.commit()
        db.refresh(db_projeto)
        return db_projeto
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Erro de banco de dados ao criar projeto")
        raise HTTPException(
            status_code=500,
            detail="Erro de banco de dados ao criar projeto"
        )
    except Exception as e:
        db.rollback()
        logger.exception("Erro interno ao criar projeto")
        raise HTTPException(
            status_code=500,
            detail="Erro interno do servidor"
        )

@projetos.get("/busca-projeto/{projeto_id}", 
              response_model=ProjetoResponse, 
              dependencies=[Depends(check_permission("tabela_projetos", "listar"))]
              )
def search_projeto(
    projeto_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    
):
    db_projeto = db.query(Projeto).options(
        joinedload(Projeto.meta).joinedload(Metas.tarefa)
    ).filter(Projeto.id == projeto_id).first()
    
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
