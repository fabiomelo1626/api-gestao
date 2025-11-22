from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.pessoaPublicaModels import PessoaPublica
from schemas.pessoaPublicaSchema import PessoaPublicaCreate, PessoaPublicaResponse

pessoa_publica = APIRouter(prefix="/api")



@pessoa_publica.post("/create-pessoa-publica/", response_model=PessoaPublicaResponse)
def create_pessoa_publica(
    pessoa_publica: PessoaPublicaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    local_id = current_user["acesso_id"]
    if not local_id:
        raise HTTPException(status_code=403, detail="Local não encontrado no token ou na requisição.")
    
    try:
        db_pessoa = PessoaPublica(**pessoa_publica.dict())
        db_pessoa.data_registro = datetime.today()
        db_pessoa.user_id = current_user["id"]

        db.add(db_pessoa)
        db.commit()
        db.refresh(db_pessoa)
        return db_pessoa

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@pessoa_publica.get("/busca-pessoa-publica/{pessoa_publica_id}", response_model=PessoaPublicaResponse)
def search_pessoa_publica(
    pessoa_publica_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_pessoa = db.query(PessoaPublica).filter(PessoaPublica.id == pessoa_publica_id).first()
    if not db_pessoa:
        raise HTTPException(status_code=404, detail="Pessoa Publica não encontrada")
    return db_pessoa


@pessoa_publica.get("/pessoas-publicas", response_model=List[PessoaPublicaResponse])
def pessoas_publicas_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(PessoaPublica).all()


@pessoa_publica.get("/pessoas-publicas-by-local_id/{local_id}", response_model=List[PessoaPublicaResponse])
def search_pessoas_local(
    local_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pessoas = db.query(PessoaPublica).filter(PessoaPublica.local_id == local_id).all()
   
    return pessoas


@pessoa_publica.put("/editar-pessoa-publica/{pessoa_publica_id}", response_model=PessoaPublicaResponse)
def update_pessoa_publica(
    pessoa_publica_id: int,
    pessoa_publica: PessoaPublicaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_pessoa = db.query(PessoaPublica).filter(PessoaPublica.id == pessoa_publica_id).first()
    if not db_pessoa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pessoa Publica não encontrada")

    try:
        for key, value in pessoa_publica.dict(exclude_unset=True).items():
            setattr(db_pessoa, key, value)

        db_pessoa.data_alteracao = datetime.now()
        db.commit()
        db.refresh(db_pessoa)
        return db_pessoa

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
