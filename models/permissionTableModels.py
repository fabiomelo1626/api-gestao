from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from conexao.conect_db import Base





class PermissionTable(Base):
    __tablename__ = "permission_table"

    id = Column(Integer, primary_key=True, index=True)
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="permission_table")
    
    nome = Column(String, unique=True)  

    permissions = relationship("UserPermission", back_populates="permission_table")
