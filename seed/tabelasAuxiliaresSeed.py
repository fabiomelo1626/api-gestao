from sqlalchemy.orm import Session
from models.auxiliaresModels import *

def seed_tabelas_auxiliares(db: Session):
    status = [
        (1, "Não iniciada"),
        (2, "Em andamento"),
        (3, "Concluída"),
        (4, "Em atraso"),
    ]

    
    db.bulk_save_objects([Status(id=c, nome=d) for c, d in status])
    db.commit()
