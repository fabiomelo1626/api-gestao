from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.userModels import User
from schemas.loginSchema import LoginSchema
from schemas.emailSchema import EmailSchema
from schemas.userSchema import ResetPasswordRequest
from schemas.acessoSchema import FirstPassword  # Schema para primeiro acesso
from utils.autenticate import hash_password, verify_password
from utils.token import create_access_token, verify_token, create_reset_password_token
from utils.email import enviar_email_com_link_reset
import traceback


login_user = APIRouter(prefix="/api")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


@login_user.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).options(joinedload(User.acessos)).filter(
            (User.username == data.username) | (User.email == data.username)
        ).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        if not db_user.status:
            raise HTTPException(status_code=403, detail="Usuário está inativo")

        if not verify_password(data.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Senha incorreta")

        acessos = db_user.acessos

        perfis_info = [{"descricao": perfil.descricao} for perfil in db_user.perfis]
        acesso_info = [{"id": acesso.id} for acesso in db_user.acessos]

        access_token = create_access_token(
            data={
                "sub": db_user.username,
                "id": db_user.id,
                "acesso_id": acesso_info,
                "perfis": perfis_info
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "username": db_user.username,
                "email": db_user.email,
                "status": db_user.status,
                "avatar": db_user.avatar,
                "created_at": db_user.created_at,
                "updated_at": db_user.updated_at,
                "acesso_id": acesso_info,
                "perfis": perfis_info,
                "first_access": db_user.first_access
            }
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@login_user.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Olá, {current_user['sub']}! Você acessou um endpoint protegido."}


@login_user.post("/esqueci-senha")
def esqueci_senha(payload: EmailSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="E-mail não encontrado")

    token = create_reset_password_token({"sub": user.email})

    link_reset = f"https://obras.gestaomunicipal.net/redefinir-senha?token={token}"

    background_tasks.add_task(enviar_email_com_link_reset, user.email, link_reset, username=user.username)

    return {"message": "E-mail enviado com instruções para redefinição de senha"}


@login_user.post("/redefinir-senha")
def redefinir_senha(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        payload_data = verify_token(payload.token)
        email = payload_data.get("sub")

        if not email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido")

    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expirado ou inválido")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    hashed_new_password = hash_password(payload.nova_senha)
    user.hashed_password = hashed_new_password

    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao atualizar a senha")

    return {"message": "Senha atualizada com sucesso!"}


@login_user.post("/primeiro-acesso")
def primeiro_acesso(payload: FirstPassword, db: Session = Depends(get_db)):
    """
    Endpoint para alterar a senha provisória no primeiro acesso.
    """
    user = db.query(User).filter(User.username == payload.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not verify_password(payload.old_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Senha atual incorreta")

    user.hashed_password = hash_password(payload.new_password)
    user.first_access = False

    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar a senha")

    return {"message": "Senha alterada com sucesso!", "user": {"username": user.username, "first_access": user.first_access}}
