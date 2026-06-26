from sqlalchemy.orm import Session
from models.auxiliaresModels import *

def seed_tabelas_auxiliares(db: Session):
    
    status = [
        (1, "Não iniciada"),
        (2, "Em andamento"),
        (3, "Concluída"),
        (4, "Em atraso"),
    ]

    categoria_mensagem = [
        (1, "COMUNICADO"),
        (2, "SOLICITAÇÃO"),
        (3, "AVISO"),
        (4, "REQUISICAO")
    ]
    
    status_mensagem = [
        (1, "ENVIADO"),
        (2, "LIDO"),
        (3, "PROCESSADO"),
        (4, "ARQUIVADO"),
        (5, "RECUSADO")
    ]
    
    db.bulk_save_objects([Status(id=c, nome=d) for c, d in status])
    db.bulk_save_objects([CategoriamMensagem(id=a, descricao=b) for a, b in categoria_mensagem])
    db.bulk_save_objects([StatusMensagem(id=a, descricao=b) for a, b in status_mensagem])
    db.commit()
