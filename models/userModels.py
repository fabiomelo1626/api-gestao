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
    estabelecimento_saude = relationship("EstabelecimentoSaude", back_populates="user")
    vinculo_profissional = relationship("VinculoProfissionalSaude", back_populates="user")
    estabelecimentoleito  = relationship("EstabelecimentoLeito", back_populates="user")
    estabelecimento_equipamento = relationship("EstabelecimentoEquipamento", back_populates="user")
    solicitacao_procedimento = relationship("SolicitacaoProcedimentoAmbulatorial", back_populates="user")
    ficha_programacao = relationship("FichaProgramacaoOrcamentaria", back_populates="user")
    autorizacao_internacao = relationship("AutorizacaoInternacaoHospitalar", back_populates="user")
    mortalidade = relationship("Mortalidade", back_populates="user")
    morbidade = relationship("Morbidade", back_populates="user")
    saude_mental = relationship("SaudeMental", back_populates="user")
    mae = relationship("Mae", back_populates="user")
    nascido_vivo = relationship("NascidoVivo", back_populates="user")
    cobertura_vacinal = relationship("CoberturaVacinal", back_populates="user")
    procedimento_ambulatorial = relationship("AutorizacaoProcedimentoAmbulatorial", back_populates="user")