from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from conexao.conect_db import Base





class PermissionTable(Base):
    __tablename__ = "permission_table"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True)  

    permissions = relationship("UserPermission", back_populates="permission_table")
