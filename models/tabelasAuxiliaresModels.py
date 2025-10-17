from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=True)



class Tipo(Base):
    __tablename__ = "tipo"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=True)



class TipoPessoa(Base):
    __tablename__ = "tipo_pessoa"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=True)

