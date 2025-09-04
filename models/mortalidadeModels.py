from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class Mortalidade(Base):
    __tablename__ = "mortalidade"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="mortalidade")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="mortalidade")

    FaixaEtaria = Column(Integer, ForeignKey("aux_faixa_etaria.id"), nullable=True)
    faixa = relationship("FaixaEtaria", back_populates="mortalidade")
    CategoriaCID = Column(String(6), nullable=True)
    SubCategoriaCID = Column(String(6), nullable=True) 
    QuantidadeMasculino = Column(Integer, nullable=True)
    QuantidadeFeminino = Column(Integer, nullable=True)
    
    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
