from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class ProjetoSetor(Base):
    __tablename__ = "projeto_setor"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="projeto")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="projeto")
    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)

    setor_id = Column(Integer, ForeignKey("setor.id"), nullable=True)
    projeto_id = Column(Integer, ForeignKey("projeto.id"), nullable=True) 

    