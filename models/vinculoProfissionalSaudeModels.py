from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, BigInteger
from sqlalchemy.orm import relationship
from conexao.conect_db import Base


class VinculoProfissionalSaude(Base):
    __tablename__ = "vinculo_profissional_saude"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="vinculo_profissional")
    local_id = Column(Integer, ForeignKey("localAcesso.id"), nullable=True)
    local = relationship("LocalAcesso", back_populates="vinculo_profissional")

    CNES = Column(Integer, nullable=True)
    CPF = Column(BigInteger, nullable=True)
    Matricula = Column(Integer, nullable=True) 
    Vinculo = Column(Integer, ForeignKey("aux_vinculo_profissional.id"), nullable=True)
    vinculo_saude = relationship("VinculoProfissional", back_populates="vinculo_profissional")
    Ocupacao = Column(BigInteger, nullable=True)
    CargaHorariaAmbulatorio = Column(Integer, nullable=True)
    CargaHorariaHospital = Column(Integer, nullable=True)
    CargaHorariaTotal = Column(Integer, nullable=True)
    DataInicioVinculo = Column(Date, nullable=True)
    DataFimVinculo = Column(Date, nullable=True)
    
    data_registro = Column(Date, nullable=True)
    data_alteracao = Column(Date, nullable=True)

    
    