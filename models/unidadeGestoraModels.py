from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql import func
from conexao.conect_db import Base
from sqlalchemy.orm import relationship

class UnidadeGestora(Base):
    __tablename__ = "unidade_gestora"

    identificador = Column(Integer, primary_key=True, unique=True, nullable=False)  
    unidade_gestora = Column(String, unique=True, nullable=False)  
    cnpj = Column(String, nullable=True)  
    codigo_ua = Column(String, unique=True, nullable=True) 
    status = Column(Boolean, default=True) 

    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="unidadegestora")
    
    obra = relationship("Obra", back_populates="unigestora")
    
    
   
   