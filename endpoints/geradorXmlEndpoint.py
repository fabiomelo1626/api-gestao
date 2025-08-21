from io import BytesIO
from fastapi import Depends, FastAPI, APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from conexao.conect_db import engine
import pandas as pd
from lxml import etree
import zipfile
import os
from endpoints.userEndpoints import get_current_user
from models.acessoModels import Acesso
from models.obraModels import Obra
from models.unidadeGestoraModels import UnidadeGestoraJoaquimGomes
from conexao.conect_db import *

xml = APIRouter(prefix="/api")


TMP_FOLDER = "./tmp"
os.makedirs(TMP_FOLDER, exist_ok=True)



def gerar_xml_tabela(
        nome_tabela,
        campos,
        tag_raiz,
        exercicio,
        mes,
        codigo_ug,
        localacesso_id,
        db
        ):
    
    try:
        print(f"🔍 Consultando tabela {nome_tabela} para {exercicio:02d}/{mes}, UG código: {codigo_ug}...")

        campos_query = ', '.join([f'{nome_tabela}."{campo}"' for campo in campos])

        tabelas_com_obra_join = {
            "cadastronacionalobras": "obra_id",
            "ordemservico": "obra_id",
            "acompanhamento": "obra_id",
            "medicao": "obra_id",
            "autorizacaolicencaambiental": "Obra",
            "documentoresponsabilidadetecnica": "obra_id"
            
        }

        join_clause = ""
        where_clause = f"""
            
            TO_DATE(CONCAT(:exercicio, '-', :mes, '-01'), 'YYYY-MM-DD') >= DATE_TRUNC('month', obra."DataInicioPrevista")

        """
        if nome_tabela == "obra":
            join_clause = """
                JOIN unidade_gestora ug ON ug.identificador = obra.unidadegestora_identificador
            """
            where_clause += """
            AND ug.identificador = :codigo
            AND obra.local_id = :localacesso_id
            AND (
            obra."Status" != 'Concluída'
            OR (
                obra."Status" = 'Concluída'
                AND DATE_TRUNC('month', obra.data_conclusao) = TO_DATE(CONCAT(:exercicio, '-', :mes, '-01'), 'YYYY-MM-DD')
                )
            )
            """
           

        elif nome_tabela in tabelas_com_obra_join:
            obra_coluna = tabelas_com_obra_join[nome_tabela]
            join_clause = f"""
                JOIN obra ON obra.id = {nome_tabela}."{obra_coluna}"
                JOIN unidade_gestora ug ON ug.identificador = obra.unidadegestora_identificador
            """
            where_clause += """
            AND ug.identificador = :codigo
            AND obra.local_id = :localacesso_id
            AND obra."Status" != 'Concluída'
            """

        else:
            join_clause = f"""
                JOIN obra ON obra."NumeroContrato" = {nome_tabela}."NumeroContrato"
                JOIN unidade_gestora ug ON ug.identificador = obra.unidadegestora_identificador
            """
            where_clause += """
            AND ug.identificador = :codigo
            AND obra.local_id = :localacesso_id
            AND obra."Status" != 'Concluída'
            """

        query = text(f"""
            SELECT {campos_query}
            FROM {nome_tabela}
            {join_clause}
            WHERE {where_clause}
        """)

        df = pd.read_sql_query(
            query, engine,
            params={"exercicio": exercicio, "mes": mes, "codigo": codigo_ug, "localacesso_id": localacesso_id}
        )

        print(f"📄 Registros encontrados: {len(df)}")

        root_siap = etree.Element("SIAP")

        etree.SubElement(root_siap, "Codigo").text = str(codigo_ug).zfill(3)
        etree.SubElement(root_siap, "Exercicio").text = str(exercicio)
        etree.SubElement(root_siap, "Mes").text = f"{mes:02d}"

       
        if df.empty:
            print(f"⚠️ Nenhum registro encontrado para {nome_tabela}")
            container = etree.SubElement(root_siap, f"{tag_raiz}s")
            registro = etree.SubElement(container, tag_raiz)
            for campo in campos:
                etree.SubElement(registro, campo).text = ""
        else:
            container = etree.SubElement(root_siap, f"{tag_raiz}s")
            for _, row in df.iterrows():
                registro = etree.SubElement(container, tag_raiz)
                for campo in campos:
                    valor = row.get(campo)
                    elem = etree.SubElement(registro, campo)
                    elem.text = "" if pd.isna(valor) else str(valor)

        xml_str = etree.tostring(
            root_siap, pretty_print=True, encoding="UTF-8", xml_declaration=True
        ).decode("utf-8")

        return xml_str

    except Exception as e:
        print(f"❌ Erro na geração do XML da tabela {nome_tabela}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro na tabela {nome_tabela}: {str(e)}")




@xml.get("/gerar-xml-zip-geral/{acesso_id}")
def gerar_xml_zip_geral(
    acesso_id:int,
    exercicio: int,
    mes: int,
    codigo: int,
    db: Session = Depends(get_db),
    #current_user: dict = Depends(get_current_user)
    ):

    acesso = db.query(Acesso).filter(
        Acesso.id == acesso_id,
    #    Acesso.usuario_id == current_user["id"],
        Acesso.ativo == True
    ).first()

    if not acesso:
        raise HTTPException(
            status_code=403,
            detail="Este acesso não pertence a este usuário ou não existe"
        )
    
    localacesso_id = acesso.localacesso_id

    identificador_ug = codigo  

    tabelas_campos = [
        {
            "nome": "obra",
            "campos": [
                "NumeroLicitacao", "NumeroContratacaoDireta", "NumeroContrato",
                "NumeroProcesso", "ObjetoContrato", "RegimeExecucaoObra", "DataInicioPrevista",
                "DataFimPrevista", "PrazoExecucao", "TipoObra", "TipoServico", "SetorBeneficiado",
                "NaturezaObra", "CodigoExecutor", "Endereco", "CEP", "Latitude", "Longitude",
                "RegistroCREA", "CPF", "CodigoQualificacao"
            ],
        },
        {
            "nome": "ordemservico",
            "campos": [
                "NumeroProcesso", "NumeroContrato", "NumeroOS", "Descricao",
                "DataEmissao", "DataInicio", "CPFResponsavel"
            ],
            "tag_raiz": "OrdemServico"
        },
        {
            "nome": "cadastronacionalobras",
            "campos": [
                "NumeroProcesso", "NumeroContrato", "NumeroCNO", "DataCadastramento"
            ],
            "tag_raiz": "CadastroNacionalObras"
        },
        {
            "nome": "acompanhamento",
            "campos": [
                "NumeroContrato", "NumeroParcela", "Data", "MesReferencia",
                "DescricaoServico", "Situacao", "Justificativa", "CPFResponsavel"
            ],
            "tag_raiz": "Acompanhamento"
        },
        {
            "nome": "medicao",
            "campos": [
                "NumeroContrato", "NumeroCNO", "Data", "CPFResponsavel",
                "PercentualMedicao", "ValorMedicao"
            ],
            "tag_raiz": "Medicao"
        },
        {
            "nome": "documentoresponsabilidadetecnica",
            "campos": [
                "NumeroContrato", "NumeroDocumento", "Data", "RegistroCREACAU",
                "CPF", "Nome", "CodigoQualificacao", "Etapa", "TipoVinculo"
            ],
            "tag_raiz": "DocumentoResponsabilidadeTecnica"
        },
        {
            "nome": "autorizacaolicencaambiental",
            "campos": [
                "NumeroContrato", "NumeroProcesso", "Tipo", "DataEmissao",
                "DataVencimento", "Empreendimento", "Endereco", "Interessado", "CompensacaoAmbiental",
                "TipoOrgaoLicenciador", "ValorCompensacao", "TipoCompensacao", "Localizacao", "Latitude",
                "Longitude"
            ],
            "tag_raiz": "AutorizacaoLicencaAmbiental"
        }
    ]

    arquivos_xml = []

    for tabela in tabelas_campos:
        nome_tabela = tabela["nome"]
        campos = tabela["campos"]
        tag_raiz = tabela.get("tag_raiz", nome_tabela.capitalize())


        xml_str = gerar_xml_tabela(nome_tabela, campos, tag_raiz, exercicio, mes, identificador_ug, localacesso_id, db)

        buffer = BytesIO()
        buffer.write(xml_str.encode("utf-8"))
        buffer.seek(0)

        #arquivos_xml.append((f"{tag_raiz}s_{codigo}_{exercicio}_{mes}.xml", buffer.read()))
        nome_arquivo_xml = f"{tag_raiz}.xml"
        arquivos_xml.append((nome_arquivo_xml, buffer.read()))

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w") as zip_file:
        for nome_arquivo, conteudo in arquivos_xml:
            zip_file.writestr(nome_arquivo, conteudo)

    ug = db.query(UnidadeGestoraJoaquimGomes).filter(UnidadeGestoraJoaquimGomes.identificador == codigo).first()
    if not ug:
        raise HTTPException(status_code=404, detail="Unidade gestora não encontrada")

    nome_formatado_ug = ug.unidade_gestora.upper().replace(" ", "_")

    nome_arquivo_zip = f"OBRA_{nome_formatado_ug}.zip"

    zip_buffer.seek(0)

    print(nome_arquivo_zip)


    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename={nome_arquivo_zip}"
        }
    )

