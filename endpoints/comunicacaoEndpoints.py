from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.comunicacaoModels import *
from models.localAcessoModels import LocalAcesso
from schemas.comunicacaoSchema import *


comunicacao = APIRouter(prefix="/api/correio", tags=["Correio Interno"])


from datetime import datetime
from zoneinfo import ZoneInfo
from models.pessoaModels import Pessoa

def agora_local():
    return datetime.now(ZoneInfo("America/Maceio")).replace(tzinfo=None)

@comunicacao.post("/enviar-mensagem")
def enviar_mensagem(
    mensagem: ComunicacaoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    ):
    try:
        if "local_id" not in current_user:
            raise HTTPException(
                status_code=400,
                detail="Local não selecionado"
            )
        local = db.query(LocalAcesso).filter(
            LocalAcesso.id == current_user["local_id"]
        ).first()
        if not local:
            raise HTTPException(status_code=404, detail="Local não encontrado")
        
        # Se destino_instituicao_id for 0, significa enviar para todas as escolas vinculadas
        destinos = []
        if mensagem.destino_instituicao_id == 0:
            local_mensagem = db.query(LocalAcesso).filter(LocalAcesso.local_id == local.id).all()
            if not local_mensagem:
                raise HTTPException(status_code=400, detail="Nenhuma escola vinculada encontrada")
            
            for e in local_mensagem:
                local = db.query(LocalAcesso).filter(LocalAcesso.id == e.id).first()
                if local:
                    destinos.append(local.id)
        elif isinstance(mensagem.destino_instituicao_id, list):
            destinos = mensagem.destino_instituicao_id
        else:
            destinos = [mensagem.destino_instituicao_id]

        # Profissional remetente
        remetente_id = None
        profissional = db.query(Pessoa).filter(Pessoa.user_id == current_user["id"]).first()
        if profissional:
            remetente_id = profissional.id

        for d_id in destinos:
            nova_mensagem = Comunicacao(**mensagem.dict())
            nova_mensagem.user_id = current_user["id"]
            nova_mensagem.local_id = local.id
            nova_mensagem.instituicao_id = local.id
            nova_mensagem.destino_instituicao_id = d_id
            nova_mensagem.remetente_id = remetente_id
            nova_mensagem.data_registro = agora_local()
            nova_mensagem.status = "ENVIADO"
            db.add(nova_mensagem)
            
        db.commit()
        return {"message": f"Mensagem enviada com sucesso para {len(destinos)} destinatário(s)."}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")



@comunicacao.get("/entrada-mensagens/{local_id}", response_model=list[ComunicacaoResponse])
def listar_mensagem_entrada(
    local_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    ):
    mensagens = db.query(Comunicacao).filter(
        Comunicacao.destino_instituicao_id == local_id
    ).order_by(Comunicacao.data_registro.desc()).all()
    return mensagens


@comunicacao.get("/mensagens-enviados/{local_id}", response_model=list[ComunicacaoResponse])
def listar_mensagens_enviadas(
    local_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
      ):
    mensagens = db.query(Comunicacao).filter(
        Comunicacao.instituicao_id == local_id
    ).order_by(Comunicacao.data_registro.desc()).all()
    return mensagens


@comunicacao.patch("/marcar-lida/{mensagem_id}")
def marcar_mensagem_lida(
    mensagem_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    ):
    mensagem = db.query(Comunicacao).filter(Comunicacao.id == mensagem_id).first()
    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    
    mensagem.status = "LIDO"
    mensagem.data_alteracao = agora_local()
    db.commit()
    db.refresh(mensagem)
    return mensagem


@comunicacao.get("/contar-pendentes/{local_id}")
def contar_mensagens_novas(
    local_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    
    ):
    qtd = db.query(Comunicacao).filter(
        Comunicacao.destino_instituicao_id == local_id,
        Comunicacao.status == "ENVIADO"
    ).count()
    return {"total_novas": qtd}

@comunicacao.get("/status-leitura/{mensagem_id}")
def status_leitura_por_destinatario(
    mensagem_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Retorna o status de leitura de todos os destinatarios de uma mensagem enviada."""
    import uuid as _uuid
    try:
        msg_id = _uuid.UUID(mensagem_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")

    original = db.query(Comunicacao).filter(Comunicacao.id == msg_id).first()
    if not original:
        raise HTTPException(status_code=404, detail="Mensagem nao encontrada")

    copias = db.query(Comunicacao).filter(
        Comunicacao.titulo == original.titulo,
        Comunicacao.conteudo == original.conteudo,
        Comunicacao.instituicao_id == original.instituicao_id
    ).all()

    resultado = []
    for copia in copias:
        destino = db.query(LocalAcesso).filter(
            LocalAcesso.id == copia.destino_instituicao_id
        ).first()
        resultado.append({
            "mensagem_id": str(copia.id),
            "destino_instituicao_id": copia.destino_instituicao_id,
            "destino_nome": destino.nome if destino else "Desconhecido",
            "status": copia.status or "ENVIADO",
            "data_leitura": str(copia.data_alteracao) if copia.data_alteracao else None
        })

    return resultado
