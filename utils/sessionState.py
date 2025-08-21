import time
from typing import Dict

usuario_acesso_ativo: Dict[int, int] = {}

def get_acesso(user_id: int, ttl_seconds: int = 2000):
    acesso = usuario_acesso_ativo.get(user_id)
    if acesso:
        acesso_id, criado_em = acesso
        if time.time() - criado_em <= ttl_seconds:
            return acesso_id
        else:
            usuario_acesso_ativo.pop(user_id)
    return None