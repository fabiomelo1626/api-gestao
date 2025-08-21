from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class Mae(Base):
    __tablename__ = "mae"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="mae")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="mae")

    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
    CPF = Column(Integer, nullable=True)
    Nome = Column(String(255), nullable=True) 
    DataNascimento = Column(Date, nullable=True)
    Raca = Column(Integer, ForeignKey("aux_raca_cor.id"), nullable=True)
    raca = relationship("RacaCor", back_populates="mae")
    QuantidadeConsulta = Column(Integer, nullable=True)
    GravidezRisco = Column(Integer, ForeignKey("aux_gravidez_risco.id"), nullable=True)
    gravidez = relationship("GravidezRisco", back_populates="mae")
