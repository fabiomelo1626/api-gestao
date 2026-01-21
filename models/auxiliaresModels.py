from sqlalchemy import Column, Integer, String, Numeric
from conexao.conect_db import Base
from sqlalchemy.orm import relationship


class Status(Base):
    __tablename__ = "aux_status"
     
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    
    meta = relationship("Metas", back_populates="status_meta")
    tarefa = relationship("Tarefa", back_populates="status_tarefa")
   
