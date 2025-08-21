from fastapi import APIRouter, HTTPException
from utils.viacep import buscar_endereco_por_cep

cep = APIRouter()

@cep.get("/enderecos/buscar_por_cep/{cep}")
def buscar_endereco(cep: str):
    try:
        dados = buscar_endereco_por_cep(cep)
        return dados
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
