from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class FichaProgramacaoOrcamentaria(Base):
    __tablename__ = "ficha_programacao_orcamentaria"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="vinculo_profissional")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="ficha_programacao")

    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
    CNES = Column(Integer, nullable=True)
    Procedimento = Column(Integer, nullable=True)
    Financiamento = Column(Integer, ForeignKey("aux_tipo_financiamento.id"), nullable=True) 
    financiamento = relationship("TipoFinanciamento", back_populates="ficha_programacao")
    Quantidade = Column(Integer, nullable=True)
    ValorUnitario = Column(Float, nullable=True)
    ValorTotal = Column(Float, nullable=True)
