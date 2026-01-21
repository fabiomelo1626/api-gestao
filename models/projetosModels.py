from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class Projeto(Base):
    __tablename__ = "projeto"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="projeto")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="projeto")
    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)

    data_conclusao = Column(Date, nullable=True)
    setor = Column(Integer, ForeignKey("setor.id"), nullable=True)
    Nome = Column(String(255), nullable=True) 
    descricao = Column(String(255), nullable=False)
    responsavel = Column(Integer, ForeignKey("pessoa.id"), nullable=True)
    status = Column(String, ForeignKey("aux_status.nome"), default="Não iniciada")
    #status_projeto = relationship("Status", back_populates="projeto")

    meta = relationship("Metas", back_populates="projeto")

    