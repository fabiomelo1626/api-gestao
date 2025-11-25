from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AtendimentoSchema(BaseModel):
    #user_id: Optional[int] = None
    #local_id: Optional[int] = None

    data_registro: Optional[datetime] = None
    data_alteracao: Optional[datetime] = None
    descricao: Optional[str] = None

    pessoa_atendimento_id: Optional[int] = None
    pessoa_publica_id: Optional[int] = None
    data: Optional[datetime] = None
    status_atendimento: Optional[int] = None
    tipo_atendimento: Optional[int] = None

    total_atendimento_dia: Optional[int] = None
    total_atendimento_semana: Optional[int] = None
    total_atendimento_mes: Optional[int] = None
    total_atendimento_ano: Optional[int] = None

    class Config:
        from_attributes = True


class AtendimentnoCreate(AtendimentoSchema):
    pass


class AtendimentnoResponse(AtendimentoSchema):
    id: int
