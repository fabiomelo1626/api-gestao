from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime


class EstabelecimentoSaudeSchema(BaseModel):
    user_id: Optional[int] = None
    local_id: Optional[int] = None

    data_registro : Optional[datetime] = None
    data_alteracao : Optional[datetime] = None
    CNES : Optional[int] = None
    CNPJ : Optional[int] = None
    NomeFantasia : Optional[str] = None
    RazaoSocial : Optional[str] = None
    Endereco : Optional[str] = None
    Cidade : Optional[str] = None
    Estado : Optional[str] = None
    Logradouro : Optional[str] = None
    Numero : Optional[str] = None
    Bairro : Optional[str] = None
    CEP : Optional[int] = None
    CPFDiretor : Optional[str] = None
    Tipo : Optional[int] = None
    AtividadePrincipal: Optional[Union[str, int]] = None
    AtividadeSecundaria: Optional[Union[str, int]] = None
    SistemaSUS : Optional[int] = None

    class Config:
        from_attributes = True


class EstabelecimentoSaudeCreate(EstabelecimentoSaudeSchema):
    class Config:
        from_attributes = True


class EstabelecimentoSaudeUpdate(EstabelecimentoSaudeSchema):
    class Config:
        from_attributes = True


class EstabelecimentoSaudeResponse(EstabelecimentoSaudeSchema):
    id: int

    class Config:
        from_attributes = True
