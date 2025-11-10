from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base

class LocalAcesso(Base):
    __tablename__ = "localAcesso"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cnpj = Column(BigInteger, nullable=True)
    Logradouro = Column(String, nullable=True)
    Numero = Column(String, nullable=True)
    Bairro = Column(String, nullable=True)
    CEP = Column(BigInteger, nullable=True)
    Cidade = Column(String, nullable=True)
    Estado = Column(String, nullable=True)
    email = Column(String, nullable=True)
    telefone = Column(BigInteger, nullable=True)
    logo = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    acessos = relationship("Acesso", back_populates="locais")
    atendimento = relationship("Atendimento", back_populates="local")
    pessoa = relationship("Pessoa", back_populates="local")
    pessoa_publica = relationship("PessoaPublica", back_populates="local")
    permission_table = relationship("PermissionTable", back_populates="local")

    
     