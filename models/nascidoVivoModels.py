from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class NascidoVivo(Base):
    __tablename__ = "nascido_vivo"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="nascido_vivo")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="nascido_vivo")

    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
    CPFMae = Column(BigInteger, nullable=True)
    NumeroDNV = Column(BigInteger, nullable=True) 
    Raca = Column(Integer, ForeignKey("aux_raca_cor.id"), nullable=True)
    raca = relationship("RacaCor", back_populates="nascido_vivo")
    DataNascimento = Column(Date, nullable=True)
    TipoParto = Column(Integer, ForeignKey("aux_tipo_parto.id"), nullable=True)
    tipo = relationship("TipoParto", back_populates="nascido_vivo")
    TempoGestacao = Column(Integer, ForeignKey("aux_tempo_gestacao.id"), nullable=True)
    tempo = relationship("TempoGestacao", back_populates="nascido_vivo")
    PesoNascimento = Column(Float, nullable=True)
  