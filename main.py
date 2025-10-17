from fastapi import FastAPI
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from conexao.conect_db import Base, engine

from endpoints.loginEndpoints import login_user
from endpoints.userEndpoints import user
from endpoints.localAcessoEndpoints import local
from endpoints.acessoEndpoints import acesso
from endpoints.pessoaEndpoints import pessoa
from endpoints.atendimentoEndpoints import atendimento


app = FastAPI(
    title="AGENDA API",
    version="1.0",
    docs_url=None,
    redoc_url=None,    
    openapi_url=None
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(login_user)
app.include_router(acesso)
app.include_router(local)
app.include_router(pessoa)
app.include_router(atendimento)


def test_connection():
    try:
        with engine.connect() as connection:
            print("Conexão bem-sucedida!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")


def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Erro ao criar as tabelas: {e}")


# Chamar a função de inicialização antes de rodar o servidor
test_connection()
create_tables()


# Rodar o servidor
if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        
    )
