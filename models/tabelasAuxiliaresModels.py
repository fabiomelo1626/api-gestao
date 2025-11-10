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


class Cargo(Base):
    __tablename__ = "cargo"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=True)


class Setor(Base):
    __tablename__ = "setor"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="pessoa")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="pessoa")

    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=True)
