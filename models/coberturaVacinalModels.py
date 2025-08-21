from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class CoberturaVacinal(Base):
    __tablename__ = "cobertura_vacinal"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="cobertura_vacinal")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="cobertura_vacinal")

    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
    FaixaEtaria = Column(Integer, ForeignKey("aux_faixa_etaria.id"), nullable=True)
    faixa = relationship("FaixaEtaria", back_populates="cobertura_vacinal")
    Vacina = Column(Integer, ForeignKey("aux_tipo_vacina.id"), nullable=True)
    vacina = relationship("TipoVacina", back_populates="cobertura_vacinal")
    QuantidadeMasculino = Column(Integer, nullable=True)
    QuantidadeFeminino = Column(Integer, nullable=True)
