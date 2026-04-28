from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class Setor(Base):
    __tablename__ = "setor"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="setor")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="setor")

    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
    Nome = Column(String(255), nullable=True) 
    descricao = Column(String(255), nullable=False)
    is_lotacao = Column(Boolean, default=False)
    
    pessoa = relationship("Pessoa", back_populates="setor")