from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class AutorizacaoProcedimentoAmbulatorial(Base):
    __tablename__ = "autorizacao_procedimento_ambulatorial"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="procedimento_ambulatorial")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="procedimento_ambulatorial")

    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
    CNES = Column(Integer, nullable=True)
    CPFAutorizador = Column(Integer, nullable=True)
    Ocupacao = Column(Integer, nullable=True)
    CNS = Column(Integer, nullable=True)
    Data = Column(Date, nullable=True)
    Procedimento = Column(Integer, nullable=True)
    CID10Principal = Column(String(4), nullable=True) 
    CID10Secundario = Column(String(4), nullable=True)
    CID10CausasAssociadas = Column(String(4), nullable=True)
    Quantidade = Column(Integer, nullable=True)
    Origem = Column(String(3), ForeignKey("aux_origem_informacoes.id"), nullable=True)
    origem = relationship("OrigemInformacoes", back_populates="procedimento_ambulatorial")

