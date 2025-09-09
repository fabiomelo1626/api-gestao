from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class EstabelecimentoSaude(Base):
    __tablename__ = "estabelecimento_saude"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="estabelecimento_saude")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="estabelecimento_saude")

    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)
    CNES = Column(Integer, nullable=True)
    CNPJ = Column(BigInteger, nullable=True, unique=True)
    NomeFantasia = Column(String(255), nullable=True) 
    RazaoSocial = Column(String(255), nullable=True)
    Endereco = Column(String(255), nullable=True)
    Cidade = Column(String(255), nullable=False)
    Estado = Column(String(2), nullable=False)
    Logradouro = Column(String(255), nullable=False)
    Numero = Column(String(10), nullable=False)
    Bairro = Column(String(255),nullable=False)
    CEP = Column(BigInteger, nullable=True)
    CPFDiretor = Column(BigInteger, nullable=True)
    Tipo = Column(Integer, ForeignKey("aux_classificacao_estabelecimento.id"), nullable=True)
    tipo = relationship("ClassificacaoEstabelecimentoSaude", back_populates="estabelecimento_saude")
    AtividadePrincipal = Column(String, ForeignKey("aux_atividade_estabelecimento.id"), nullable=True)
    atividade_estabelecimento = relationship("AtividadeEstabelecimentoSaude",foreign_keys=[AtividadePrincipal], back_populates="estabelecimento_saude")
    AtividadeSecundaria = Column(String, ForeignKey("aux_atividade_estabelecimento.id"), nullable=True)
    atividade_secundaria = relationship("AtividadeEstabelecimentoSaude",foreign_keys=[AtividadeSecundaria], back_populates="estabelecimento")
    SistemaSUS = Column(Integer, ForeignKey("aux_sus.id"), nullable=True)
    sistema = relationship("Sus", back_populates="estabelecimento_saude")

