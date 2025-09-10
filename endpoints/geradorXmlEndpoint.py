from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
import os
import xml.etree.ElementTree as ET
import zipfile

from conexao.conect_db import get_db
from endpoints.userEndpoints import get_current_user
from models.autorizacaoInternacaoHospitalarModels import AutorizacaoInternacaoHospitalar
from models.autorizacaoInternacaoHospitalarModels import AutorizacaoInternacaoHospitalar
from models.autorizacaoProcedimentoAmbulatorialModels import AutorizacaoProcedimentoAmbulatorial
from models.coberturaVacinalModels import CoberturaVacinal
from models.estabelecimentoEquipamentoModels import EstabelecimentoEquipamento
from models.estabelecimentoLeitoModels import EstabelecimentoLeito
from models.estabelecimentoSaudeModels import EstabelecimentoSaude
from models.fichaProgramacaoOrcamentariaModels import FichaProgramacaoOrcamentaria
from models.maeModels import Mae
from models.morbidadeModels import Morbidade
from models.mortalidadeModels import Mortalidade
from models.nascidoVivoModels import NascidoVivo
from models.saudeMentalModels import SaudeMental
from models.solicitacaoProcedimentoAmbulatorialModels import SolicitacaoProcedimentoAmbulatorial
from models.vinculoProfissionalSaudeModels import VinculoProfissionalSaude


xml = APIRouter()

def gerar_xml_tabela(db: Session, modelo, nome: str, exercicio: int, mes: int, local_id: int, xml_path: str):
    registros = db.query(modelo).filter_by(local_id=local_id).all()

    root = ET.Element("SIAP")

    ET.SubElement(root, "Codigo").text = str(local_id)
    ET.SubElement(root, "Exercicio").text = str(exercicio)
    ET.SubElement(root, "Mes").text = f"{mes:02d}"

    if registros:
        for registro in registros:
            item_elem = ET.SubElement(root, nome) 
            for coluna in registro.__table__.columns:
                valor = getattr(registro, coluna.name)
                campo = ET.SubElement(item_elem, coluna.name)
                campo.text = str(valor) if valor is not None else ""

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)



@xml.get("/exportar_xml_zip/")
def exportar_xml_zip(
    exercicio: int,
    mes: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    local_id = current_user["acesso_id"]
    tabelas = {
        "AutorizacaoInternacaoHospitalar": AutorizacaoInternacaoHospitalar,
        "AutorizacaoProcedimentoAmbulatorial": AutorizacaoProcedimentoAmbulatorial,
        "CoberturaVacinal": CoberturaVacinal,
        "EstabelecimentoEquipamento": EstabelecimentoEquipamento,
        "EstabelecimentoLeito": EstabelecimentoLeito,
        "EstabelecimentoSaude": EstabelecimentoSaude,
        "FichaProgramacaoOrcamentaria": FichaProgramacaoOrcamentaria,
        "Mae": Mae,
        "Morbidade": Morbidade,
        "Mortalidade": Mortalidade,
        "NascidoVivo": NascidoVivo,
        "SaudeMental": SaudeMental,
        "SolicitacaoProcedimentoAmbulatorial": SolicitacaoProcedimentoAmbulatorial,
        "VinculoProfissionalSaude": VinculoProfissionalSaude,
    }

    pasta_saida = "xml_temp"
    os.makedirs(pasta_saida, exist_ok=True)

    arquivos_xml = []
    for nome, modelo in tabelas.items():
        xml_path = os.path.join(pasta_saida, f"{nome}.xml")
        gerar_xml_tabela(db, modelo, nome, exercicio, mes, local_id, xml_path)
        arquivos_xml.append(xml_path)

    nome_zip = f"SAUDE_{local_id}_{exercicio}{mes:02d}.zip"
    caminho_zip = os.path.join(pasta_saida, nome_zip)

    with zipfile.ZipFile(caminho_zip, "w") as zipf:
        for file in arquivos_xml:
            zipf.write(file, os.path.basename(file))

    return FileResponse(
        caminho_zip,
        media_type="application/zip",
        filename=nome_zip
    )
