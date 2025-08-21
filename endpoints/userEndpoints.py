from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from conexao.conect_db import get_db
from models.userModels import User
from schemas.userSchema import UserCreate, UserResponse, UpdatePassword, UserUpdate, FirstPassword
from utils.autenticate import hash_password, verify_password
from utils.token import verify_token
from utils.randomUtils import generate_random_password
from utils.email import enviar_email_boas_vindas


user = APIRouter(prefix="/api")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
    return payload


def require_perfil(permissoes: list[str]):
    def wrapper(user=Depends(get_current_user)):
        print("🧪 Perfis recebidos no token:", user.get("perfis", []))
        user_perfis = [perfil["descricao"] for perfil in user.get("perfis", [])]
        print("🧪 Descrições:", user_perfis)
        if not any(perfil in permissoes for perfil in user_perfis):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. É necessário um dos perfis: {permissoes}"
            )
        return user
    return wrapper


@user.post("/create-user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):   
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Nome de usuário já está em uso")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="E-mail já está em uso")

    senha_temporaria = generate_random_password()
    hashed_password = hash_password(senha_temporaria)

    novo_usuario = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        avatar=user.avatar,
        status=True,
        fullname=user.fullname,
        first_access=True
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    background_tasks.add_task(
        enviar_email_boas_vindas,
        destinatario=novo_usuario.email,
        senha=senha_temporaria,
        username=novo_usuario.username,
        link="https://obras.gestaomunicipal.net/login"
    )

    return novo_usuario


@user.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    for u in users:
        if u.status is None:
            u.status = False
    return users


@user.put("/edit-user/{user_id}", response_model=UserResponse)
def update_user(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # Verifica se novo username/email está em uso por outro usuário
    if db.query(User).filter(User.username == update_data.username, User.id != user_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome de usuário já está em uso por outro usuário")
    if db.query(User).filter(User.email == update_data.email, User.id != user_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já está em uso por outro usuário")

    user.username = update_data.username
    user.fullname = update_data.fullname
    user.email = update_data.email
    user.avatar = update_data.avatar

    db.commit()
    db.refresh(user)
    return user


@user.get("/busca-user/{user_id}", response_model=UserResponse)
def search_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user


@user.put("/edit-password", response_model=UserResponse)
def update_password(request: UpdatePassword, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    user.hashed_password = hash_password(request.new_password)
    db.commit()
    db.refresh(user)
    return user


@user.put("/inativar-user/{user_id}", response_model=UserResponse)
def inativar_usuario(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    usuario = db.query(User).filter(User.id == user_id).first()

    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    usuario.status = not usuario.status if usuario.status is not None else False

    db.commit()
    db.refresh(usuario)
    return usuario

@user.put("/primeiro-acesso", response_model=UserResponse)
def primeiro_acesso(payload: FirstPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not verify_password(payload.old_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Senha atual incorreta")

    user.hashed_password = hash_password(payload.new_password)
    user.first_access = False

    db.commit()
    db.refresh(user)
    return user



