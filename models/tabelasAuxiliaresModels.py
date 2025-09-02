from sqlalchemy import Column, Integer, String, Float
from conexao.conect_db import Base
from sqlalchemy.orm import relationship


class ClassificacaoEstabelecimentoSaude(Base):
    __tablename__ = "aux_classificacao_estabelecimento"
     
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    
    estabelecimento_saude = relationship("EstabelecimentoSaude", back_populates="tipo")
   

class AtividadeEstabelecimentoSaude(Base):
    __tablename__ = "aux_atividade_estabelecimento"

    id = Column(String, primary_key=True, index=True)
    atividade = Column(String, nullable=True)
    descricao = Column(String, nullable=False)
    
    estabelecimento_saude = relationship("EstabelecimentoSaude", back_populates="atividade_estabelecimento", foreign_keys="[EstabelecimentoSaude.AtividadePrincipal]")
    estabelecimento = relationship("EstabelecimentoSaude", back_populates="atividade_secundaria", foreign_keys="[EstabelecimentoSaude.AtividadeSecundaria]")



class Sus(Base):
    __tablename__ = "aux_sus"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)

    estabelecimento_saude = relationship("EstabelecimentoSaude", back_populates="sistema")
    estabelecimento_equipamento = relationship("EstabelecimentoEquipamento", back_populates="disponibilidade")
    


class VinculoProfissional(Base):
    __tablename__ = "aux_vinculo_profissional"
    id = Column(String, primary_key=True, index=True)
    FormaContratacao = Column(String, nullable=True)
    descricao = Column(String, nullable=False)

    vinculo_profissional = relationship("VinculoProfissionalSaude", back_populates="vinculo_saude")



class TiposLeito(Base):
    __tablename__ = "aux_tipos_leito"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)

    estabelecimento_leito = relationship("EstabelecimentoLeito", back_populates="tipo")
    autorizacao_internacao = relationship("AutorizacaoInternacaoHospitalar", back_populates="especialidade")


class TipoEquipamento(Base):
    __tablename__ = "aux_tipo_equipamento"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    
    estabelecimento_equipamento = relationship("EstabelecimentoEquipamento", back_populates="tipo")
    

class TipoFinanciamento(Base):
    __tablename__ = "aux_tipo_financiamento"

    id = Column(String, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    
    
    ficha_programacao = relationship("FichaProgramacaoOrcamentaria", back_populates="financiamento")


class OrigemInformacoes(Base):
    __tablename__ = "aux_origem_informacoes"

    id = Column(String, primary_key=True, index=True)
    descricao = Column(String, nullable=False)

    solicitacao_procedimento = relationship("SolicitacaoProcedimentoAmbulatorial", back_populates="origem")
    procedimento_ambulatorial = relationship("AutorizacaoProcedimentoAmbulatorial", back_populates="origem")

    

class IdentificacaoAIH(Base):
    __tablename__ = "aux_identificacao_aih"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    
    autorizacao_internacao = relationship("AutorizacaoInternacaoHospitalar", back_populates="identificacao")



class ModalidadeInternacao(Base):
    __tablename__ = "aux_modalidade_internacao"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    
    autorizacao_internacao = relationship("AutorizacaoInternacaoHospitalar", back_populates="modalidade")



class CaraterInternacao(Base):
    __tablename__ = "aux_carater_internacao"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    
    autorizacao_internacao = relationship("AutorizacaoInternacaoHospitalar", back_populates="carater_internacao")



class MotivoSaida(Base):
    __tablename__ = "aux_motivo_saida"

    id = Column(String, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    
    autorizacao_internacao = relationship("AutorizacaoInternacaoHospitalar", back_populates="motivo_saida")



class FaixaEtaria(Base):
    __tablename__ = "aux_faixa_etaria"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    
    mortalidade = relationship("Mortalidade", back_populates="faixa")
    morbidade = relationship("Morbidade", back_populates="faixa")
    saude_mental = relationship("SaudeMental", back_populates="faixa")
    cobertura_vacinal = relationship("CoberturaVacinal", back_populates="faixa")


class RacaCor(Base):
    __tablename__ = "aux_raca_cor"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)

    mae = relationship("Mae", back_populates="raca")
    nascido_vivo = relationship("NascidoVivo", back_populates="raca")



class GravidezRisco(Base):
    __tablename__ = "aux_gravidez_risco"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=True)


    mae = relationship("Mae", back_populates="gravidez")



class TipoParto(Base):
    __tablename__ = "aux_tipo_parto"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    nascido_vivo = relationship("NascidoVivo", back_populates="tipo")
    

class TempoGestacao(Base):
    __tablename__ = "aux_tempo_gestacao"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    nascido_vivo = relationship("NascidoVivo", back_populates="tempo")



class TipoVacina(Base):
    __tablename__ = "aux_tipo_vacina"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    cobertura_vacinal = relationship("CoberturaVacinal", back_populates="vacina")
