from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class Atendimento(Base):
    __tablename__ = "atendimento"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="atendimento")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="atendimento")

    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
    descricao = Column(String, nullable=True)
    pessoa_id = Column(Integer, ForeignKey("pessoa.id"), nullable=True)
    #pessoa = relationship("Pessoa", back_populates="atendimento")
    status_atendimento = Column(String, ForeignKey("aux_status.nome"), default="Não iniciada")
    data_atendimento = Column(Date, nullable=True)
    

    total_atendimento_dia = Column(Integer, nullable=True)
    total_atendimento_semana = Column(Integer, nullable=True)
    total_atendimento_mes = Column(Integer, nullable=True)
    total_atendimento_ano = Column(Integer, nullable=True)
    
    