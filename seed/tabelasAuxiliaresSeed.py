from sqlalchemy.orm import Session
'''from models.tabelasAuxiliaresModels import (
    QualificacaoProfissional,
    TipoObra,
    TipoServicos,
    SetorBeneficiado,
    TipoFornecedor,
    RegimeExecucaoObra,
    NaturezaObra,
    Situacao,
    Etapa,
    TipoVinculo,
    TipoLicenca,
    TipoOrgaoLicenciador,
    CodigoQualificacao,
    Compensacao
)

def seed_tabelas_auxiliares(db: Session):
    qualificacoes = [
        (1, "Engenheiro Civil"),
        (2, "Engenheiro Eletricista"),
        (3, "Engenheiro de Telecomunicações"),
        (4, "Engenheiro – Mecânica"),
        (5, "Engenheiro – Minas"),
        (6, "Engenheiro – Químico"),
        (7, "Engenheiro – Naval"),
        (8, "Engenheiro – Outros"),
        (9, "Geólogo"),
        (10, "Técnico – Edificações"),
        (11, "Técnico – Estradas"),
        (12, "Técnico – Eletrônica"),
        (13, "Técnico – Telecomunicações"),
        (14, "Técnico – Eletrotécnico"),
        (15, "Técnico – Agrícola"),
        (16, "Técnico – Refrigeração"),
        (17, "Técnico – Mecânica"),
        (18, "Técnico – Mineração"),
        (19, "Técnico – Outros"),
        (20, "Arquiteto"),
        (99, "Outros"),
    ]

    tipos_obra = [
        (1, "Adutora"),
        (2, "Aeroporto"),
        (3, "Aterro Sanitário"),
        (4, "Balança Rodoviária"),
        (5, "Barragem"),
        (6, "Biblioteca"),
        (7, "Canal"),
        (8, "Creche"),
        (9, "Delegacia de Policia"),
        (10, "Drenagem Urbana"),
        (11, "Escola"),
        (12, "Estação Elevatória"),
        (13, "Hospital"),
        (14, "Limpeza Pública"),
        (15, "Linha de Distribuição de Energia Elétrica Rural"),
        (16, "Linha de Distribuição de Energia Elétrica Urbana"),
        (17, "Módulo Sanitário"),
        (18, "Muro de Contenção de Aterros"),
        (19, "Obra de Arte Corrente"),
        (20, "Obra de Arte Especial"),
        (21, "Passarela"),
        (22, "Perfuração de Poço Tubular"),
        (23, "Posto Fiscal"),
        (24, "Praça"),
        (25, "Praça de Pedágio"),
        (26, "Rede de Coleta de Esgoto"),
        (27, "Rede de Distribuição de Água"),
        (28, "Rede de Distribuição de Energia Elétrica"),
        (29, "Rodovia não Pavimentada"),
        (30, "Rodovia Pavimentada"),
        (31, "Sinalização Viária"),
        (32, "Subestação de Energia Elétrica"),
        (33, "Terminal Rodoviário"),
        (34, "Unidade Administrativa"),
        (35, "Unidade Desportiva"),
        (36, "Unidade de Saúde"),
        (37, "Unidade Habitacional"),
        (38, "Unidade Prisional"),
        (39, "Via Urbana não Pavimentada"),
        (40, "Via Urbana Pavimentada"),
        (41, "Outros"),
        (42, "Parque Aquático"),
        (43, "Instituto Médico Legal"),
        (44, "Estadio"),
        (45, "Via Urbana a ser Pavimentada"),
        (46, "Centro Cirúrgico"),
        (47, "Quadra de Esporte"),
        (48, "Cobertura"),
        (49, "Sanitários Públicos"),
        (50, "Salão de Idosos"),
        (51, "Prédio Público"),
        (52, "Cobertura de Quadra Esportiva"),
        (53, "Centro Cultural de Convivência"),
        (54, "Esgotamento Sanitário"),
        (55, "Reposição Asfáltica"),
        (56, "Rede Coletora de Esgoto"),
        (57, "Estacão de Tratamento de Água"),
        (58, "Estrada Vicinal não Pavimentada"),
        (59, "Posto de Saúde"),
        (60, "Casas Populares"),
        (61, "Policlínica- Clínica"),
        (62, "Estrada Vicinal Pavimentada"),
        (63, "Drenagem de Águas Pluviais"),
        (64, "Ruas e Avenidas"),
        (65, "Iluminação Pública"),
    ]

    tipos_servico = [
        (1, "Ampliação"),
        (2, "Construção Nova"),
        (3, "Manutenção"),
        (4, "Readequação"),
        (5, "Reforma"),
        (6, "Restauração"),
        (7, "Pavimentação Asfáltica"),
        (8, "Reforma e Ampliação"),
        (9, "Conservação"),
        (10, "Reconstrução"),
        (11, "Supervisão, Acompanhamento e Controle de Obras"),
        (12, "Pavimentação"),
        (13, "Recuperação"),
        (14, "Fabricação"),
        (15, "Serviços Técnicos Especializados"),
        (16, "Outros"),
    ]
    
    tipo_fornecedor = [
        (1, "Pessoa Física"),
        (2, "Pessoa Jurídica"),
        # (3, "UG"),
        # (4, "Credor Estrangeiro")
    ]
    
    regime_execucao = [
        (1, "Empreitada por preço global"),
        (2, "Empreitada por preço unitário"),
        (3, "Empreitada Integral"),
        (4, "Tarefa"),
        (5, "Execução Direta"),
        (6, "Contratação Integrada"),
        (7, "Contratação Semi-Integrada"),
    ]

    natureza_obra = [
        (1, "Reforma"),
        (2, "Construção"),
        (3, "Ampliação"),
        (4, "Fabricação"),
        (5, "Recuperação"),
        (6, "Construção e Reforma"),
        (7, "Serviços Técnicos Especializados"),
    ]

    situacoes = [
        (1, "Ativa, na hipótese de obra regular em pleno desenvolvimento da atividade de construção civil;"),
        (2, "Atrasada"),
        (3, "Paralisada, quando informada a interrupção temporária da atividade pela contratada;"),
        (4, "Suspensa, por ato de ofício;"),
        (5, "Encerrada, quando a obra for regularizada."),
    ]

    etapas = [
        (1, "Projeto"),
        (2, "Orçamento"),
        (3, "Execução"),
        (4, "Fiscalização"),
    ]

    tipo_vinculo = [
        (1, "Servidor Efetivo"),
        (2, "Servidor Contratado"),
        (3, "Servidor Comissionado"),
    ]

    tipo_licenca = [
        (1, "Licença Prévia"),
        (2, "Licença de Instalação"),
        (3, "Licença de Operação"),
        (4, "Autorização Ambiental"),
        (5, "Licença Simplificada"),
    ]
    
    compensacao_ambiental = [
        (1, "SIM"),
        (2, "NÃO")
    ]
    
    
    setor_beneficiado = [
        (1, "Cultura"),
        (2, "Educação"),
        (3, "Esporte"),
        (4, "Infra-estrutura e Transporte"),
        (5, "Meio Ambiente, Recursos Hídricos e Saneamento"),
        (6, "Saúde"),
        (7, "Segurança Pública"),
        (8, "Turismo"),
        (9, "Urbanização e Habitação"),
        (10, "Ministério Público"),
        (11, "Administração Central"),
        (12, "Ação Social"),
        (13, "Justiça"),
        (14, "Assistência Social"),
        (15, "Limpeza Pública"),
        (16, "Agricultura"),
        (17, "Comunicação"),
        (18, "Energia")
    ]
    
    codigo_qualificacao = [
        (1, "Engenheiro Civil"),
        (2, "Engenheiro Eletricista"),
        (3, "Engenheiro de Telecomunicações"),
        (4, "Engenheiro – Mecânica"),
        (5, "Engenheiro – Minas"),
        (6, "Engenheiro – Químico"),
        (7, "Engenheiro – Naval"),
        (8, "Engenheiro – Outros"),
        (9, "Geólogo"),
        (10, "Técnico – Edificações"),
        (11, "Técnico – Estradas"),
        (12, "Técnico – Eletrônica"),
        (13, "Técnico – Telecomunicações"),
        (14, "Técnico – Eletrotécnico"),
        (15, "Técnico – Agrícola"),
        (16, "Técnico – Refrigeração"),
        (17, "Técnico – Mecânica"),
        (18, "Arquiteto"),
        (19, "Fiscal")
    ]
    
    orgaos_licenciadores = [
        (1, "Municipal"),
        (2, "Estadual"),
        (3, "Federal"),
    ]
    
   
    
    db.bulk_save_objects([QualificacaoProfissional(codigo=c, descricao=d) for c, d in qualificacoes])
    db.bulk_save_objects([TipoObra(id=c, descricao=d) for c, d in tipos_obra])
    db.bulk_save_objects([TipoServicos(id=c, descricao=d) for c, d in tipos_servico])
    db.bulk_save_objects([TipoFornecedor(codigo=c, tipo=d) for c, d in tipo_fornecedor])
    db.bulk_save_objects([RegimeExecucaoObra(id=c, descricao=d) for c, d in regime_execucao])
    db.bulk_save_objects([NaturezaObra(id=c, descricao=d) for c, d in natureza_obra])
    db.bulk_save_objects([Situacao(id=c, descricao=d) for c, d in situacoes])
    db.bulk_save_objects([Etapa(id=c, descricao=d) for c, d in etapas])
    db.bulk_save_objects([TipoVinculo(id=c, descricao=d) for c, d in tipo_vinculo])
    db.bulk_save_objects([TipoLicenca(id=c, descricao=d) for c, d in tipo_licenca])
    db.bulk_save_objects([TipoOrgaoLicenciador(id=c, descricao=d) for c, d in orgaos_licenciadores])
    db.bulk_save_objects([SetorBeneficiado(id=c, descricao=d) for c , d in setor_beneficiado])
    db.bulk_save_objects([CodigoQualificacao(id=c, descricao=d) for c, d in codigo_qualificacao])
    db.bulk_save_objects([Compensacao(id=c, descricao=d) for c ,d in compensacao_ambiental])
    
    db.commit()'''
