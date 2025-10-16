from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
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
    CPF = Column(BigInteger, nullable=True)
    RG = Column(BigInteger, nullable=True)
    Titulo = Column(BigInteger, nullable=True)
    Nome = Column(String(255), nullable=True) 
    DataNascimento = Column(Date, nullable=True)
    Cidade = Column(String(255), nullable=False)
    Estado = Column(String(2), nullable=False)
    Logradouro = Column(String(255), nullable=False)
    Numero = Column(String(10), nullable=False)
    Bairro = Column(String(255),nullable=False)
    CEP = Column(BigInteger, nullable=True)
    email = Column(String, nullable=True)
    tipo = Column(Integer, ForeignKey("tipo_pessoa.id"), nullable=True)
    tipopessoa = relationship("TipoPessoa", back_populates="pessoa")
    

    atendimento = relationship("Atendimento", back_populates="pessoa")