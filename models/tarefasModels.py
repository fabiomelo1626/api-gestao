from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class Tarefa(Base):
    __tablename__ = "tarefa"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="tarefa")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="tarefa")
    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
    
    data_conclusao = Column(Date, nullable=True)
    nome = Column(String(255), nullable=True) 
    descricao = Column(String(255), nullable=False)
    responsavel = Column(Integer, ForeignKey("pessoa.id"), nullable=True)
    meta_id = Column(Integer, ForeignKey("metas.id"), nullable=True)
    meta_tarefa = relationship("Metas", back_populates="tarefa")
    status = Column(String, ForeignKey("aux_status.nome"), default="Não iniciada")
    status_tarefa = relationship("Status", back_populates="tarefa")
    setor_id = Column(Integer, ForeignKey("setor.id"), nullable=True)
    