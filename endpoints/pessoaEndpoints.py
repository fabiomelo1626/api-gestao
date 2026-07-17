from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, join

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.pessoaModels import Pessoa
from schemas.pessoaSchema import *
from utils.middlewareDependence import check_permission


pessoa = APIRouter(prefix="/api")



@pessoa.post("/create-pessoa/", 
             response_model=PessoaResponse, 
             dependencies=[Depends(check_permission("tabela_pessoa", "criar"))]
             )
def create_pessoa(
    pessoa: PessoaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    
    
    try:
        db_pessoa = Pessoa(**pessoa.dict())
        db_pessoa.data_registro = datetime.today()
        db_pessoa.user_id = current_user["id"]
        db_pessoa.local_id = pessoa.local_id

        db.add(db_pessoa)
        db.commit()
        db.refresh(db_pessoa)
        return db_pessoa

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@pessoa.get("/busca-pessoa/{pessoa_id}", 
            response_model=PessoaResponse, 
            dependencies=[Depends(check_permission("tabela_pessoa", "listar"))]
            )
def search_pessoa(
    pessoa_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    
    db_pessoa = db.query(Pessoa)\
    .options(joinedload(Pessoa.cargo),
             joinedload(Pessoa.setor))\
    .filter(Pessoa.id == pessoa_id)\
    .first()

    if not db_pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    
   

    return db_pessoa

@pessoa.get("/pessoas", 
            response_model=List[PessoaResponse], 
            dependencies=[Depends(check_permission("tabela_pessoa", "listar"))]
            )
def pessoas_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return db.query(Pessoa).all()


@pessoa.get("/pessoas-by-local_id/{local_id}", 
            response_model=List[PessoaResponse], 
            dependencies=[Depends(check_permission("tabela_pessoa", "listar"))]
            )
def search_pessoas_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    pessoas = db.query(Pessoa).filter(Pessoa.local_id == local_id).all()
   
    return pessoas


@pessoa.put("/editar-pessoa/{pessoa_id}", 
             response_model=PessoaResponse,            
             dependencies=[Depends(check_permission("tabela_pessoa", "listar"))]
             )
def update_pessoa(
    pessoa_id: int,
    pessoa: PessoaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
    if not db_pessoa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pessoa não encontrada")

    try:
        for key, value in pessoa.dict(exclude_unset=True).items():
            setattr(db_pessoa, key, value)

        db_pessoa.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_pessoa)
        return db_pessoa

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
