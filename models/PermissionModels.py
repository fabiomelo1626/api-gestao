from sqlalchemy import Column, Integer, Boolean, ForeignKey, Date, String
from sqlalchemy.orm import relationship
from conexao.conect_db import Base




class PermissionTables(Base):
    __tablename__ = "permission_tables"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="permission_tables")

    data_registro =  Column(Date, nullable=True)
    data_alteracao =  Column(Date, nullable=True)

    nome = Column(String, nullable=True)
    tabela_metas = Column(Boolean, default=False)
    tabela_responsaveis = Column(Boolean, default=False)
    tabela_setor = Column(Boolean, default=False)
    tabela_tarefas = Column(Boolean, default=False)
    tabela_pessoa = Column(Boolean, default=False)
    tabela_atendimento = Column(Boolean, default=False)
    tabela_acessos = Column(Boolean, default=False)
    tabela_cargos = Column(Boolean, default=False)
    tabela_projetos = Column(Boolean, default=False)
    tabela_user = Column(Boolean, default=False)
    tabela_permissoes = Column(Boolean, default=False)

    listar = Column(Boolean, default=False)
    criar = Column(Boolean, default=False)
    editar = Column(Boolean, default=False)
    deletar = Column(Boolean, default=False)

    user = relationship("User", back_populates="permissions")


class UserPermissions(Base):
    __tablename__ = "user_permissions"
    user_cadastra_id =     user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    cadastrador = relationship("LocalAcesso",foreign_keys=[user_cadastra_id], back_populates="user_cadastra")

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User",foreign_keys=[user_id], back_populates="permissions")
    permission_table_id = Column(Integer, ForeignKey("permission_tables.id"), nullable=True)
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)

    data_registro =  Column(Date, nullable=True)
    data_alteracao =  Column(Date, nullable=True)
