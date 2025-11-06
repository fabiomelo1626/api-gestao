from sqlalchemy import Column, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from conexao.conect_db import Base




class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    data_registro =  Column(Date, nullable=True)
    data_alteracao =  Column(Date, nullable=True)

    listar = Column(Boolean, default=False)
    criar = Column(Boolean, default=False)
    editar = Column(Boolean, default=False)
    deletar = Column(Boolean, default=False)

    user = relationship("User", back_populates="permissions")
