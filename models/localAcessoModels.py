from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base

class LocalAcesso(Base):
    __tablename__ = "localAcesso"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cnpj = Column(BigInteger, nullable=True)
    logradouro = Column(String, nullable=True)
    numero = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    cep = Column(BigInteger, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    email = Column(String, nullable=True)
    telefone = Column(BigInteger, nullable=True)
    logo = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    cor = Column(String, default="#1113d3")
    #default = "#1113d3"
    acessos = relationship("Acesso", back_populates="locais")
    permission_tables = relationship("PermissionTables", back_populates="local")
    setor = relationship("Setor", back_populates="local")
    meta = relationship("Metas", back_populates="local")
    pessoa = relationship("Pessoa", back_populates="local")
    tarefa = relationship("Tarefa", back_populates="local")
    cargo = relationship("Cargo", back_populates="local")
    projeto = relationship("Projeto", back_populates="local")
    atendimento = relationship("Atendimento", back_populates="local")

    
     