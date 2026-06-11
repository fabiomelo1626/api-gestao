from fastapi import FastAPI
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from conexao.conect_db import Base, engine

from endpoints.loginEndpoints import login_user
from endpoints.userEndpoints import user
from endpoints.localAcessoEndpoints import local
from endpoints.acessoEndpoints import acesso
from endpoints.metasEndpoints import metas
from endpoints.pessoaEndpoints import pessoa
from endpoints.tarefasEndpoints import tarefas
from endpoints.auxiliaresEndpoints import auxiliares
from endpoints.userPermissionEndpoints import permission
from endpoints.permissionTableEndpoint import table
from endpoints.setorEndpoints import setor
from endpoints.cargoEndpoints import cargo
from endpoints.projetosEndpoints import projetos
from endpoints.atendimentoEndpoints import atendimento
from endpoints.dashboardEndpoints import dashboard
from seed.popular import popular


app = FastAPI(
    title="AGENDA API",
    version="1.0",
    #docs_url=None,
    #redoc_url=None,    
    #openapi_url=None
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
app.include_router(metas)
app.include_router(pessoa)
app.include_router(tarefas)
app.include_router(auxiliares)
app.include_router(permission)
app.include_router(setor)
app.include_router(table)
app.include_router(cargo)
app.include_router(projetos)
app.include_router(atendimento)
app.include_router(dashboard)

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


test_connection()
create_tables()
#popular()


# Rodar o servidor
if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        
    )
