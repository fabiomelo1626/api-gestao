import uuid
from sqlalchemy import UUID, Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class Comunicacao(Base):
    __tablename__ = "comunicacao"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="comunicacao")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", foreign_keys=[local_id], back_populates="comunicacao")

    remetente_id = Column(Integer, ForeignKey("pessoa.id"), nullable=True)   
    remetente = relationship("Pessoa", foreign_keys=[remetente_id], back_populates="comunicacoes_registradas")

    instituicao_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    instituicao = relationship("LocalAcesso", foreign_keys=[instituicao_id], back_populates="mensagens_enviadas")

    destinatario_id = Column(Integer, ForeignKey("pessoa.id"), nullable=True)
    destinatario = relationship("Pessoa", foreign_keys=[destinatario_id], back_populates="mensagens_recebidas")

    destino_instituicao_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    destino = relationship("LocalAcesso",foreign_keys=[destino_instituicao_id], back_populates="mensagens_recebidas")

    categoria = Column(Integer, ForeignKey("aux_categoria_mensagem.id"), nullable=True)

    titulo = Column(String(255), nullable=True)
    conteudo = Column(String(1024), nullable=True)

    status = Column(String, ForeignKey("aux_status_mensagem.descricao"))

    anexo = Column(String, nullable=True)

    
    data_registro = Column(DateTime, nullable=True)
    data_alteracao = Column(DateTime, nullable=True)
