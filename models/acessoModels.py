from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from conexao.conect_db import Base

class Acesso(Base):
    __tablename__ = "acesso"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("user.id"))
    usuarios = relationship("User", back_populates="acessos")

    localacesso_id = Column(Integer, ForeignKey("localAcesso.id"))
    locais = relationship("LocalAcesso", back_populates="acessos")

    data_registro = Column(Date)
    data_alteracao = Column(Date, nullable=True)

    ativo = Column(Boolean, nullable=True)

