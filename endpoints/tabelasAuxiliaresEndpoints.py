from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from conexao.conect_db import get_db
from models.tabelasAuxiliaresModels import (
    ClassificacaoEstabelecimentoSaude,
    AtividadeEstabelecimentoSaude,
    Sus,
    VinculoProfissional,
    TiposLeito,
    TipoEquipamento,
    TipoFinanciamento,
    OrigemInformacoes,
    IdentificacaoAIH,
    ModalidadeInternacao,
    CaraterInternacao,
    MotivoSaida,
    FaixaEtaria,
    RacaCor,
    GravidezRisco,
    TipoParto,
    TempoGestacao,
    TipoVacina
)

from endpoints.userEndpoints import get_current_user


auxiliares = APIRouter(prefix="/api/auxiliares", tags=["Tabelas Auxiliares"])



def listar_todos(model, db):
    return db.query(model).order_by(model.id).all()


@auxiliares.get("/classificacao-estabelecimento", summary="Listar Classificações Estabelecimentos")
def listar_classificacoes(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(ClassificacaoEstabelecimentoSaude).order_by(ClassificacaoEstabelecimentoSaude.id).all()


@auxiliares.get("/atividade-estabelecimento", summary="Listar Atividades Estabelecimentos")
def listar_atividades(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(AtividadeEstabelecimentoSaude).order_by(AtividadeEstabelecimentoSaude.id).all()


@auxiliares.get("/sus", summary="Listar sus")
def listar_sus(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(Sus).order_by(Sus.id).all()

@auxiliares.get("/vinculos-profissionais", summary="Listar todos os vinculos profissionais")
def get_vinculo_profissional(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(VinculoProfissional, db)

@auxiliares.get("/tipos-leito", summary="Listar todos os tipos leito")
def get_tipo_leito(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(TiposLeito, db)

@auxiliares.get("/tipo-equipamento", summary="Listar todos os tipos equipamentos")
def get_tipo_equipamento(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(TipoEquipamento, db)

@auxiliares.get("/tipo-financiamento", summary="Listar todas os tipos financiamentos")
def get_tipo_financiamento(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(TipoFinanciamento, db)

@auxiliares.get("/origem-informacoes", summary="Listar todas as origens informações")
def get_origem_informacoes(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(OrigemInformacoes, db)

@auxiliares.get("/identificacao-aih", summary="Listar todos os tipos de licenças")
def get_identificacao_aih(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(IdentificacaoAIH).order_by(IdentificacaoAIH.id).all()

@auxiliares.get("/tipo-modalidade-internacao", summary="Listar todas as modaldidades internação")
def get_modalidade_internacao(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(ModalidadeInternacao, db)

@auxiliares.get("/carater-internacao", summary="Listar todos os carater informação")
def get_carater_internacao(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(CaraterInternacao, db)

@auxiliares.get("/motivo_saida", summary="Listar todos os motivos saida")
def get_motivo_saida(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(MotivoSaida, db)

@auxiliares.get("/faixa-etaria", summary="Listar todas as faixas etarias")
def get_faixa_etaria(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(FaixaEtaria, db)


@auxiliares.get("/raca-cor", summary="Listar todas as faixas etarias")
def get_raca_cor(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(RacaCor, db)


@auxiliares.get("/gravidez-risco", summary="Listar todas as gravidez de risco")
def get_gravidez_risco(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(GravidezRisco, db)


@auxiliares.get("/tipo-parto", summary="Listar todos os tipos parto")
def get_tipo_parto(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(TipoParto, db)


@auxiliares.get("/tempo-gestacao", summary="Listar todos os tempos de gestação")
def get_tempo_gestacao(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(TempoGestacao, db)



@auxiliares.get("/tipo_vacina", summary="Listar todos os tipos de vacina")
def get_tipo_vacina(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return listar_todos(TipoVacina, db)
