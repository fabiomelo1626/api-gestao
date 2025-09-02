# local_acesso.py
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
    
    estabelecimento_saude = relationship("EstabelecimentoSaude", back_populates="local")
    vinculo_profissional = relationship("VinculoProfissionalSaude", back_populates="local")
    estabelecimentoleito = relationship("EstabelecimentoLeito", back_populates="local")
    estabelecimento_equipamento = relationship("EstabelecimentoEquipamento", back_populates="local")
    ficha_programacao = relationship("FichaProgramacaoOrcamentaria", back_populates="local")
    solicitacao_procedimento = relationship("SolicitacaoProcedimentoAmbulatorial", back_populates="local")
    autorizacao_internacao = relationship("AutorizacaoInternacaoHospitalar", back_populates="local")
    mortalidade = relationship("Mortalidade", back_populates="local")
    morbidade = relationship("Morbidade", back_populates="local")
    saude_mental = relationship("SaudeMental", back_populates="local")
    mae = relationship("Mae", back_populates="local")
    nascido_vivo = relationship("NascidoVivo", back_populates="local")
    cobertura_vacinal = relationship("CoberturaVacinal", back_populates="local")
    procedimento_ambulatorial = relationship("AutorizacaoProcedimentoAmbulatorial", back_populates="local")
      