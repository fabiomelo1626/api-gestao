from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class Pessoa(Base):
    __tablename__ = "pessoa"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="pessoa")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="pessoa")

    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
    cpf = Column(BigInteger, nullable=True)
    rg = Column(BigInteger, nullable=True)
    titulo = Column(BigInteger, nullable=True)
    nome = Column(String(255), nullable=True) 
    datanascimento = Column(Date, nullable=True)
    cidade = Column(String(255), nullable=True)
    estado = Column(String(2), nullable=True)
    logradouro = Column(String(255), nullable=True)
    numero = Column(String(10), nullable=True)
    bairro = Column(String(255),nullable=True)
    cep = Column(BigInteger, nullable=True)
    email = Column(String, nullable=True)
    telefone = Column(Integer, nullable=True)
    is_secretario = Column(Boolean, default=False)
    is_funcionario = Column(Boolean, default=False) 
    setor_id = Column(Integer, ForeignKey("setor.id"), nullable=True)
    cargo_id = Column(Integer, ForeignKey("cargo.id"), nullable=True)
    telefone = Column(Integer, nullable=True)
    
    setor = relationship("Setor", back_populates="pessoa")
    cargo = relationship("Cargo", back_populates="pessoa")