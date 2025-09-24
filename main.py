from fastapi import FastAPI
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from conexao.conect_db import Base, engine

from endpoints.tabelasAuxiliaresEndpoints import auxiliares
from endpoints.estabelecimentoSaudeEndpoints import estabelecimento
from endpoints.vinculoProfissionalSaudeEndpoints import vinculo
from endpoints.estabelecimentoLeitoEndpoints import estabelecimento_leito
from endpoints.estabelecimentoEquipamentoEndpoints import estabelecimento_equipamento
from endpoints.fichaProgramacaoOrcamentariaEndpoints import ficha
from endpoints.solicitacaoProcedimentoAmbulatorialEndpoints import solicitacao_procedimento
from endpoints.autorizacaoProcedimentoAmbulatorialEndpoints import autorizacao
from endpoints.autorizacaoInternacaoHospitalarEndpoints import autorizacao_internacao
from endpoints.mortalidadeEndpoints import mortalidade
from endpoints.morbidadeEndpoints import morbidade
from endpoints.saudeMentalEndpoints import saude_mental
from endpoints.maeEndpoints import mae
from endpoints.nascidoVivoEndpoints import nascido_vivo
from endpoints.coberturaVacinalEndpoints import cobertura
from endpoints.loginEndpoints import login_user
from endpoints.userEndpoints import user
from endpoints.localAcessoEndpoints import local
from endpoints.acessoEndpoints import acesso
from endpoints.relatorioPdfEndpoints import pdf
from endpoints.geradorXmlEndpoint import xml
from seed.popular import popular


app = FastAPI(
    title="SAÚDE SIAP API",
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
app.include_router(auxiliares)
app.include_router(estabelecimento)
app.include_router(vinculo)
app.include_router(estabelecimento_leito)
app.include_router(estabelecimento_equipamento)
app.include_router(ficha)
app.include_router(solicitacao_procedimento)
app.include_router(autorizacao)
app.include_router(autorizacao_internacao)
app.include_router(mortalidade)
app.include_router(morbidade)
app.include_router(saude_mental)
app.include_router(mae)
app.include_router(nascido_vivo)
app.include_router(cobertura)
app.include_router(login_user)
app.include_router(local)
app.include_router(user)
app.include_router(acesso)
app.include_router(pdf)
app.include_router(xml)


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
#popular()


# Rodar o servidor
if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        
    )
