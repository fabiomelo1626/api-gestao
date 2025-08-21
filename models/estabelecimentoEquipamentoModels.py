from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class EstabelecimentoEquipamento(Base):
    __tablename__ = "estabelecimento_equipamento"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="estabelecimento_equipamento")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="estabelecimento_equipamento")

    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
    CNES = Column(Integer, nullable=True)
    Codigo = Column(Integer, nullable=True)
    Tipo = Column(Integer, ForeignKey("aux_tipo_equipamento.id"), nullable=True)
    tipo = relationship("TipoEquipamento", back_populates="estabelecimento_equipamento")
    Quantidade = Column(Integer, nullable=True) 
    QuantidadeSUS = Column(Integer, nullable=True)
    DisponibilidadeSUS = Column(Integer, ForeignKey("aux_sus.id"), nullable=True)
    disponibilidade = relationship("Sus", back_populates="estabelecimento_equipamento")
