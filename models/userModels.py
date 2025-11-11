from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from conexao.conect_db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    fullname = Column(String, nullable=True)
    status = Column(Boolean, default=True)  
    avatar = Column(String, nullable=True)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    first_access = Column(Boolean, default=True)
    
   
    acessos = relationship("Acesso", back_populates="usuarios")
    atendimento = relationship("Atendimento", back_populates="user")
    pessoa = relationship("Pessoa", back_populates="user")
    pessoa_publica = relationship("PessoaPublica", back_populates="user")
    permissions = relationship("UserPermission", back_populates="user")
    setor = relationship("Setor", back_populates="user")