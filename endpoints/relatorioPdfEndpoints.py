from fastapi import Depends, APIRouter, HTTPException
import requests
from models.autorizacaoInternacaoHospitalarModels import AutorizacaoInternacaoHospitalar
from models.autorizacaoProcedimentoAmbulatorialModels import AutorizacaoProcedimentoAmbulatorial
from models.coberturaVacinalModels import CoberturaVacinal
from sqlalchemy.orm import Session
from conexao.conect_db import get_db
from fastapi.responses import FileResponse
import os

pdf = APIRouter(prefix="/api")


@pdf.get("/pdf-autorizacao-internacao/{autorizacao_id}")
def gerar_pdf_autorizacao_internacao(autorizacao_id: int, db: Session = Depends(get_db)):
    autorizacao = db.query(AutorizacaoInternacaoHospitalar).filter(AutorizacaoInternacaoHospitalar.id == autorizacao_id).first()
    if not autorizacao:
        raise HTTPException(status_code=404, detail="Autorização Internação não encontrada")
    
    payload = {
        "data_registro": autorizacao.data_registro.isoformat() if autorizacao.data_registro else None,
        "CNES": autorizacao.CNES,
        "NumeroAIH": autorizacao.NumeroAIH,
        "DataInternacao": autorizacao.DataInternacao.isoformat() if autorizacao.DataInternacao else None,
        "MotivoSaida": autorizacao.MotivoSaida
    }


    resp = requests.post("http://189.126.106.183:5000/api/autorizacao/relatorio", json=payload)
    if resp.status_code == 200:
        filename = f"relatorio_autorizacao_{autorizacao.id}.pdf"
        filepath = os.path.join(os.getcwd(), filename)

        with open(filepath, "wb") as f:
            f.write(resp.content)

        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/pdf"
        )
    else:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {resp.text}")


