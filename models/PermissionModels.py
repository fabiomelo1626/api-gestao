from sqlalchemy import Column, Integer, Boolean, ForeignKey, Date, String
from sqlalchemy.orm import relationship
from conexao.conect_db import Base




class PermissionTable(Base):
    __tablename__ = "permission_table"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
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
    tabela_user = Column(Boolean, default=True)
    tabela_permissoes = Column(Boolean, default=False)

    listar = Column(Boolean, default=False)
    criar = Column(Boolean, default=False)
    editar = Column(Boolean, default=False)
    deletar = Column(Boolean, default=False)

    user = relationship("User", back_populates="permissions")
    #permission_table = relationship("PermissionTable", back_populates="permissions")


class UserPermission(Base):
    __tablename__ = "user_permission"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    permission_table_id = Column(Integer, ForeignKey("permission_table.id"), nullable=True)

    data_registro =  Column(Date, nullable=True)
    data_alteracao =  Column(Date, nullable=True)

