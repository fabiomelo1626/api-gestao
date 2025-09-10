from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from conexao.conect_db import get_db
from models.acessoModels import Acesso
from schemas.acessoSchema import AcessoCreate, AcessoResponse
from typing import List
from datetime import date
from utils.sessionState import usuario_acesso_ativo
from endpoints.userEndpoints import get_current_user
from utils.token import create_access_token

acesso = APIRouter(prefix="/api", tags=["Acessos"])


@acesso.post("/create-acesso", response_model=AcessoResponse)
def criar_acesso(acesso_data: AcessoCreate, db: Session = Depends(get_db)):
    existente = db.query(Acesso).filter(
        Acesso.usuario_id == acesso_data.usuario_id,
        Acesso.localacesso_id == acesso_data.localacesso_id
    ).first()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já está vinculado a esse cliente."
        )

    novo = Acesso(**acesso_data.dict(), data_registro=date.today(), ativo=True)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@acesso.get("/acesso/usuario/{usuario_id}", response_model=List[AcessoResponse])
def listar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    acessos = db.query(Acesso)\
        .options(joinedload(Acesso.usuarios), joinedload(Acesso.locais))\
        .filter(Acesso.usuario_id == usuario_id)\
        .all()
    return acessos


@acesso.get("/acesso-usuario-byId/{user_id}", response_model=List[AcessoResponse])
def list_acessos_usuarios(user_id: int, db: Session = Depends(get_db)):
    list_acessos = db.query(Acesso)\
        .options(joinedload(Acesso.locais))\
        .filter(Acesso.usuario_id == user_id)\
        .all()
    return list_acessos


@acesso.post("/selecionar-local/{local_id}")
def definir_local(
    local_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    new_token = create_access_token(data={
        "sub": current_user["sub"],
        "id": current_user["id"],
        # "acesso_id": current_user["acesso_id"],
        # "perfis": current_user["perfis"],
        "local_id":local_id
    })

    return {
        "access_token": new_token,
        "token_type": "bearer",
        "sub":current_user["sub"],
        "id":current_user["id"],
        # "acesso_id":current_user["acesso_id"],
        "local_id": local_id,
    }



 
@acesso.get("/acesso/{acesso_id}", response_model=AcessoResponse)
def listar_acesso(acesso_id: int, db: Session = Depends(get_db)):
    acesso_obj = db.query(Acesso)\
        .options(joinedload(Acesso.usuarios), joinedload(Acesso.locais))\
        .filter(Acesso.id == acesso_id)\
        .first()

    if not acesso_obj:
        raise HTTPException(status_code=404, detail="Acesso não encontrado")
    return acesso_obj


@acesso.get("/acessos", response_model=List[AcessoResponse])
def listar_todos_acessos(db: Session = Depends(get_db)):
    acessos = db.query(Acesso)\
        .options(joinedload(Acesso.usuarios), joinedload(Acesso.locais))\
        .all()
    return acessos


@acesso.get("/acessos-ativos", response_model=List[AcessoResponse])
def listar_acessos_ativos(db: Session = Depends(get_db)):
    acessos = db.query(Acesso)\
        .filter(Acesso.ativo == True)\
        .options(joinedload(Acesso.usuarios), joinedload(Acesso.locais))\
        .all()
    return acessos


@acesso.patch("/acesso/{acesso_id}/ativar-inativar")
def ativar_ou_inativar_acesso(acesso_id: int, db: Session = Depends(get_db)):
    acesso_obj = db.query(Acesso).filter(Acesso.id == acesso_id).first()

    if not acesso_obj:
        raise HTTPException(status_code=404, detail="Acesso não encontrado")

    acesso_obj.ativo = not acesso_obj.ativo
    acesso_obj.data_alteracao = date.today()

    db.commit()
    db.refresh(acesso_obj)

    status_msg = "ativado" if acesso_obj.ativo else "inativado"
    return {"detail": f"Acesso {status_msg} com sucesso", "acesso": acesso_obj}


@acesso.post("/selecionar-acesso/{acesso_id}")
def selecionar_acesso(acesso_id: int, db: Session = Depends(get_db)):
    acesso = db.query(Acesso).filter_by(id=acesso_id, usuario_id=get_current_user["id"]).first()
    if not acesso:
        raise HTTPException(status_code=404, detail="Acesso não encontrado para este usuário")

    usuario_acesso_ativo[get_current_user["id"]] = acesso_id
    return {"message": f"Acesso {acesso_id} definido como ativo"}


@acesso.delete("/acesso/{acesso_id}")
def remover_acesso(acesso_id: int, db: Session = Depends(get_db)):
    acesso_obj = db.query(Acesso).filter(Acesso.id == acesso_id).first()
    if not acesso_obj:
        raise HTTPException(status_code=404, detail="Acesso não encontrado")

    db.delete(acesso_obj)
    db.commit()
    return {"detail": "Acesso removido com sucesso"}
