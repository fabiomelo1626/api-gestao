from sqlalchemy.orm import Session
from models.tabelasAuxiliaresModels import *

def seed_tabelas_auxiliares(db: Session):
    status = [
        (1, "Em andamento"),
        (2, "Em espera"),
        (3, "Concluído"),
        (4, "Cancelado"),
    ]

    tipo = [
        (1, "Solicitação"),
        (2, "Reunião"),
    ]

    tipo_pessoa = [
        (1, "Funcionário"),
        (2, "Cidadão Comum"),
        (3, "Religioso"),
    ]
    
    cargo = [
        (1, "Diretor(a)"),
        (2, "Vereador(a)"),
        (3, "Secretário(a)"),
        (4, "Prefeito(a)")
    ]
    
    setor = [
        (1, "Prefeitura"),
        (2, "Câmara"),
        (3, "Secretaria"),
    ]

    
   
    
    db.bulk_save_objects([Status(id=c, descricao=d) for c, d in status])
    db.bulk_save_objects([Tipo(id=c, descricao=d) for c, d in tipo])
    db.bulk_save_objects([TipoPessoa(id=c, descricao=d) for c, d in tipo_pessoa])
    db.bulk_save_objects([Cargo(id=c, descricao=d) for c, d in cargo])
    db.bulk_save_objects([Setor(id=c, descricao=d) for c, d in setor])
    db.commit()
