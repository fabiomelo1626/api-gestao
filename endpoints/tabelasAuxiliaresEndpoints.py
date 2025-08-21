from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from conexao.conect_db import get_db
from models.tabelasAuxiliaresModels import QualificacaoProfissional, TipoObra,\
    SetorBeneficiado, TipoFornecedor, UnidadeExecutora, RegimeExecucaoObra, NaturezaObra, \
    Situacao, Etapa, TipoVinculo, TipoLicenca, TipoServicos, TipoOrgaoLicenciador

from endpoints.userEndpoints import get_current_user


auxiliares = APIRouter(prefix="/api/auxiliares", tags=["Tabelas Auxiliares"])



def listar_todos(model, db):
    return db.query(model).order_by(model.id).all()


@auxiliares.get("/qualificacoes", summary="Listar Qualificações Profissionais")
def listar_qualificacoes(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(QualificacaoProfissional).order_by(QualificacaoProfissional.codigo).all()


@auxiliares.get("/setores", summary="Listar Setores Beneficiados")
def listar_setores(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(SetorBeneficiado).order_by(SetorBeneficiado.id).all()


@auxiliares.get("/unidades-executoras", summary="Listar Unidades Executoras")
def listar_unidades_executoras(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(UnidadeExecutora).order_by(UnidadeExecutora.codigo).all()



@auxiliares.get("/regimes", summary="Listar todos os regimes de execução de obra")
def get_regimes(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(RegimeExecucaoObra, db)

@auxiliares.get("/naturezas", summary="Listar todas as naturezas de obra")
def get_naturezas(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(NaturezaObra, db)

@auxiliares.get("/situacoes", summary="Listar todas as situações de obra")
def get_situacoes(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(Situacao, db)

@auxiliares.get("/etapas", summary="Listar todas as etapas de obra")
def get_etapas(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(Etapa, db)

@auxiliares.get("/tipos-vinculo", summary="Listar todos os tipos de vínculo")
def get_tipos_vinculo(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(TipoVinculo, db)

@auxiliares.get("/tipos-fornecedor", summary="Listar todos os tipos de Fornecedores")
def get_tipos(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(TipoFornecedor).order_by(TipoFornecedor.codigo).all()

@auxiliares.get("/tipo-licenca", summary="Listar todos os tipos de licenças")
def get_tipos(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(TipoLicenca, db)

@auxiliares.get("/tipo-obra", summary="Listar todos os tipos de obras")
def get_tipos(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(TipoObra, db)

@auxiliares.get("/tipo-servico", summary="Listar todos os tipos de Serviços")
def get_tipos(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(TipoServicos, db)

@auxiliares.get("/orgaos-licenciadores", summary="Listar todos os tipos de órgão licenciador")
def get_orgaos_licenciadores(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(TipoOrgaoLicenciador, db)
