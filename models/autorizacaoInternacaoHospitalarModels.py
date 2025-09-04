from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class AutorizacaoInternacaoHospitalar(Base):
    __tablename__ = "autorizacao_internacao_hospitalar"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="autorizacao_internacao")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="autorizacao_internacao")
    
    CNES = Column(Integer, nullable=True)
    NumeroAIH = Column(BigInteger, nullable=True)
    Identificacao = Column(Integer, ForeignKey("aux_identificacao_aih.id"), nullable=True) 
    identificacao = relationship("IdentificacaoAIH", back_populates="autorizacao_internacao")
    EspecialidadeLeito = Column(Integer, ForeignKey("aux_tipos_leito.id"), nullable=True)
    especialidade = relationship("TiposLeito", back_populates="autorizacao_internacao")
    ModalidadeInternacao = Column(Integer, ForeignKey("aux_modalidade_internacao.id"), nullable=True)
    modalidade = relationship("ModalidadeInternacao", back_populates="autorizacao_internacao")
    AIHAnterior = Column(BigInteger, nullable=True)
    DataEmissao = Column(Date, nullable=True)
    DataInternacao = Column(Date, nullable=True)
    DataSaida = Column(Date, nullable=True)
    ProcedimentoSolicitado = Column(BigInteger, nullable=True)
    CaraterInternacao = Column(Integer, ForeignKey("aux_carater_internacao.id"), nullable=True)
    carater_internacao = relationship("CaraterInternacao", back_populates="autorizacao_internacao")
    MotivoSaida = Column(String, ForeignKey("aux_motivo_saida.id"), nullable=True)
    motivo_saida = relationship("MotivoSaida", back_populates="autorizacao_internacao")
    CNSSolicitante = Column(BigInteger, nullable=True)
    CNSResponsavel = Column(BigInteger, nullable=True)
    CNSAutorizador = Column(BigInteger, nullable=True)
    DiagnosticoPrincipal = Column(String(4), nullable=True)
    CNSPaciente = Column(BigInteger, nullable=True)
    
    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
