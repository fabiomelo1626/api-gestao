from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class Morbidade(Base):
    __tablename__ = "morbidade"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="morbidade")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="morbidade")

    FaixaEtaria = Column(Integer, ForeignKey("aux_faixa_etaria.id"), nullable=True)
    faixa = relationship("FaixaEtaria", back_populates="morbidade")
    CategoriaCID = Column(String(6), nullable=True)
    SubCategoriaCID = Column(String(6), nullable=True) 
    QuantidadeMasculino = Column(Integer, nullable=True)
    QuantidadeFeminino = Column(Integer, nullable=True)
<<<<<<< HEAD
    
    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
=======
  
>>>>>>> cf3bda59fc7e0ba69ebeb6ce3a900f36767d9ece
