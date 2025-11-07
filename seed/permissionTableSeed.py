from sqlalchemy.orm import Session
from models.permissionTableModels import PermissionTable


def seed_tabelas_permissoes(db: Session):
    tabelas = [
        (1, "pessoa"),
        (2, "pessoa_publica"),
        (3, "atendimento"),
    ]

    db.bulk_save_objects([PermissionTable(id=c, nome=d) for c, d in tabelas])