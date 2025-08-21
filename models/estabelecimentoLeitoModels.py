from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class EstabelecimentoLeito(Base):
    __tablename__ = "estabelecimento_leito"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="estabelecimentoleito")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="estabelecimentoleito")

    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
    CNES = Column(Integer, nullable=True)
    TipoLeito = Column(Integer, ForeignKey("aux_tipos_leito.id"), nullable=True)
    tipo = relationship("TiposLeito", back_populates="estabelecimento_leito")
    Quantidade = Column(Integer, nullable=True) 
    QuantidadeSUS = Column(Integer, nullable=True)