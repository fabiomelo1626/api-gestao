from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class Metas(Base):
    __tablename__ = "metas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="meta")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="meta")
    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)

    data_conclusao = Column(Date, nullable=True)
    setor = Column(Integer, ForeignKey("setor.id"), nullable=True)
    nome = Column(String(255), nullable=True) 
    descricao = Column(String(255), nullable=False)
    responsavel = Column(Integer, ForeignKey("pessoa.id"), nullable=True)
    projeto_id = Column(Integer, ForeignKey("projeto.id"), nullable=True)
    projeto = relationship("Projeto", back_populates="meta")
    status = Column(String, ForeignKey("aux_status.nome"), default="Não iniciada")
    status_meta = relationship("Status", back_populates="meta")

    tarefa = relationship("Tarefa", back_populates="meta_tarefa")

    