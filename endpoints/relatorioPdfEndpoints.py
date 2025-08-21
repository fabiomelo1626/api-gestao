from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from conexao.conect_db import get_db

from weasyprint import HTML
from io import BytesIO


from models.obraModels import Obra       
from utils.gerar_html import gerar_html_obra 

relatorio = APIRouter(prefix="/api")


@relatorio.get("/obras/{obra_id}/relatorio", response_class=StreamingResponse)
def gerar_relatorio_obra(obra_id: int, db: Session = Depends(get_db)):
    obra = db.query(Obra).filter(Obra.id == obra_id).first()
    if not obra:
        raise HTTPException(status_code=404, detail="Obra não encontrada")

    html = gerar_html_obra(obra)
    pdf_bytes = HTML(string=html).write_pdf()

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="relatorio_obra_{obra_id}.pdf"'
        }
    )