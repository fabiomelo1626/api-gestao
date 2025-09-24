from sqlalchemy.orm import Session
from models.tabelasAuxiliaresModels import *



def seed_tabelas_auxiliares(db: Session):
    tipo_estabelecimento = [
        (1, "POSTO DE SAÚDE"),
        (2, "CENTRO DE SAÚDE/UNIDADE BÁSICA"),
        (4, "POLICLÍNICA"),
        (5, "HOSPITAL GERAL"),
        (7, "HOSPITAL ESPECIALIZADO"),
        (15, "UNIDADE MISTA"),
        (20, "PRONTO SOCORRO GERAL"),
        (22, "CONSULTÓRIO ISOLADO"),
        (36, "CLINICA/CENTRO DE ESPECIALIDADE"),
        (39, "UNIDADE DE APOIO DIAGNOSE E TERAPIA (SADT ISOLADO)"),
        (40, "UNIDADE MÓVEL TERRESTRE"),
        (42, "UNIDADE MÓVEL DE NÍVEL PRE-HOSPITALAR NA ÁREA DE URGÊNCIA"),
        (43, "FARMÁCIA"),
        (50, "UNIDADE DE VIGILÂNCIA EM SAÚDE"),
        (60, "COOPERATIVA OU EMPRESA DE CESSÃO DE TRABALHADORES NA SAÚDE"),
        (61, "CENTRO DE PARTO NORMAL - ISOLADO"),
        (62, "HOSPITAL/DIA - ISOLADO"),
        (68, "CENTRAL DE GESTÃO EM SAÚDE"),
        (69, "CENTRO DE ATENÇÃO HEMOTERAPIA E OU HEMATOLÓGICA"),
        (70, "CENTRO DE ATENÇÃO PSICOSSOCIAL"),
        (71, "CENTRO DE APOIO A SAÚDE DA FAMÍLIA"),
        (72, "UNIDADE DE ATENÇÃO A SAÚDE INDÍGENA"),
        (73, "PRONTO ATENDIMENTO"),
        (74, "POLO ACADEMIA DA SAÚDE"),
        (75, "TELESSAUDE"),
        (76, "CENTRAL DE REGULACAO MEDICA DAS URGÊNCIAS"),
        (77, "SERVIÇO DE ATENÇÃO DOMICILIAR ISOLADO (HOME CARE)"),
        (79, "OFICINA ORTOPÉDICA"),
        (80, "LABORATÓRIO DE SAÚDE PUBLICA"),
        (81, "CENTRAL DE REGULACAO DO ACESSO"),
        (82, "CENTRAL DE NOTIFICAÇÃO, CAPTAÇÃO E DISTRIBUIÇÃO DE ÓRGÃOS ESTADUAL"),
        (83, "POLO DE PREVENÇÃO DE DOENÇAS E AGRAVOS E PROMOÇÃO DA SAÚDE"),
        (84, "CENTRAL DE ABASTECIMENTO"),
        (85, "CENTRO DE IMUNIZAÇÃO"),
    ]

    atividade_estabelecimento = [
        ("00", "Não se aplica", "Utilizar apenas para a atividade secundária, quando não "
        "existirem outras atividades desenvolvidas no local, pois a "
        "atividade principal é obrigatória."),
        ("01", "Consulta Ambulatorial", "Atendimento dispensado a indivíduos cuja condição de saúde "
        "estável lhes permita comparecer ao estabelecimento e retornar "
        "ao local de origem, realizado por profissionais de saúde de nível "
        "superior, com a finalidade de fornecer parecer, instrução ou "
        "examinar determinada situação, a fim de decidir sobre um plano "
        "de ação ou prescrição terapêutica dentro da sua área de "
        "atuação. Exige instalações físicas ambulatoriais, como "
        "consultórios, e a caracterização como Atendimento Ambulatorial "
        "de Média Complexidade."),
        ("02", "Apoio Diagnóstico", "Ações e serviços que se utilizam de recursos físicos e tecnológicos "
        "(exemplos: Raios-x, Ultrassonografia, Ressonância Magnética, Análises Clínicas/Laboratoriais, "
        "Eletrocardiografia, Endoscopia, etc.) com o objetivo de auxiliar, de forma complementar, a "
        "determinação da natureza de uma doença ou estado, ou a diferenciação entre elas, melhorando a "
        "tomada de decisão assistencial. Exige a informação dos equipamentos e o Atendimento Ambulatorial "
        "de Média ou Alta Complexidade."),
        ("03", "Terapias Especiais", "Atividades voltadas exclusivamente para a realização de hemodiálise, "
        "quimioterapia, radioterapia ou cirurgias ambulatoriais (neste caso basicamente a situação de "
        "procedimentos em Hospitais-Dia). Exige a informação dos equipamentos e o Atendimento Ambulatorial"
        " de Média ou Alta Complexidade."),
        ("04", "Reabilitação", "Conjunto de ações e serviços orientados a desenvolver ou ampliar a capacidade "
        "funcional e desempenho dos indivíduos, proteger a saúde e prevenir agravos, de modo a contribuir para "
        "autonomia, acesso à direitos e participação em todas as esferas da vida social. Engloba a reabilitação"
        " visual, auditiva, física e mental (APAE, CAPS e entidades similares). Não engloba a reabilitação oral."
        " Exige a informação do Atendimento Ambulatorial de Média Complexidade."),
        ("05", "Concessão, Manutenção e Adaptação de OPM", "As Órteses, Próteses, Materiais Especiais e Meios de "
        "Locomoção (OPM) constituem ferramentas do processo terapêutico da reabilitação, contribuindo fundamentalmente"
        " na superação de barreiras, devendo ser prescritas de forma individualizada por profissional capacitado."
        " A concessão de OPM deve estar obrigatoriamente atrelada à adaptação, manutenção e treino de uso da mesma."),
        ("06", "Atenção Domiciliar", "Ações e serviços prestados de forma substitutiva ou complementar à internação"
        " hospitalar ou atendimento ambulatorial, caracterizados pelo conjunto de tratamento de doenças, reabilitação,"
        " promoção à saúde e prevenção, englobando internação e/ou assistência prestadas em domicílio. Exige a informação"
        " do Atendimento Ambulatorial de Média Complexidade."),
        ("07", "Assistência a Emergências", "Cuidados destinados a pacientes de demanda espontânea com agravos que necessitam"
        " de atendimento imediato por risco iminente de morte. Atividades de Pronto-Socorro e Pronto- Atendimento. (SAMU, UPAs)."
        " Exige a informação do Atendimento Ambulatorial ou Hospitalar de Média Complexidade, instalações de Urgência e "
        "Emergência (Exceto para estabelecimentos móveis, como Ambulâncias, Motolâncias, Ambulanchas, etc.) e Equipamentos para "
        "Manutenção da Vida."),
        ("08", "Entrega/Dispensação de Medicamentos", "Conjunto de ações relativas ao fornecimento de medicamentos diretamente ao"
        " paciente e a orientação para o seu uso racional, mediante apresentação de prescrição por profissional habilitado, e"
        " obrigatório para Hospitais."),
        ("09", "Internação", "Cuidados ou tratamentos prestados a um indivíduo, por razões clínicas e/ou cirúrgicas, que demandem"
        " a ocupação de um leito por um período igual ou superior a 24 horas. Exige a informação de Leitos para Informação, Instalação "
        "Hospitalar na Caracterização de Média e/ou Alta Complexidade."),
        ("10", "Assistência Intermediária", "Conjunto de ações realizadas entre a internação e o atendimento ambulatorial, para realização"
        " de procedimentos clínicos, cirúrgicos, diagnósticos e terapêuticos, que requeiram a permanência do paciente em um leito por um"
        " período inferior a 24 horas. Exige a informação do Atendimento Ambulatorial de Média Complexidade."),
        ("11", "Atenção Psicossocial", "Conjunto de ações intersetoriais de caráter territorial e comunitário que visa à substituição"
        " do modelo asilar manicomial, por meio de cuidados que possibilitem a reabilitação psicossocial das pessoas em sofrimento"
        " psíquico ou transtorno mental, incluindo aquelas com necessidades 294 decorrentes do uso de álcool e outras drogas, garantindo "
        "atenção contínua às situações de crise em saúde mental e articulação do cuidado com outros pontos de atenção. Apenas unidades "
        "públicas. Exige a informação do Atendimento Ambulatorial de Média Complexidade e o Serviço Especializado."),
        ("12", "Atenção Básica", "Conjunto de ações e serviços longitudinais de saúde no âmbito individual e coletivo, de caráter "
        "territorial e comunitário, que abrange o cuidado/tratamento, a promoção e proteção da saúde, a prevenção de agravos, a vigilância"
        " em saúde, a reabilitação e a redução de danos à saúde, coordenando ou integrando o cuidado fornecido em outros pontos de atenção. "
        "Apenas unidades públicas, no caso as Unidades Básicas de Saúde. Exige a informação do Atendimento Ambulatorial de Atenção Básica e"
        " a existência de equipes da Estratégia Saúde da Família (eSF ) ou Consultório na Rua (eCR)."),
        ("13", "Assistência Obstétrica e Neonatal", "Conjunto de cuidados ou tratamentos prestados à gestante, parturiente e recém-nascido,"
        " por razões obstétricas ou neonatais. Apenas centros materno-infantis."),
        ("14", "Telessaúde", "Serviços que utilizam tecnologias da informação e comunicação como meio para desenvolver ações de apoio a"
        " Atenção à Saúde e de Educação Permanente em Saúde, com o fim de realizar apoio diagnóstico, ações educativas, esclarecer dúvidas"
        " dos profissionais de saúde e gestores de saúde."),
        ("15", "Atenção Hematológica e/ou Hemoterápica", "Conjunto de ações que integram a assistência especializada em coagulopatias e "
        "hemoglobinopatias e/ou o conjunto de ações referentes a captação do doador, o ciclo de produção do sangue, testes sorológicos, "
        "testes imunohematológicos, distribuição e transfusão de sangue e componentes e demais atividades hemoterápicas. Exige a informação "
        "do Atendimento Ambulatorial de Média e/ou Alta Complexidade e o Serviço Especializado."),
        ("16", "Promoção da Saúde, Prevenção de Doenças e Agravos e Produção do Cuidado", "Conjunto de ações e serviços de saúde, de caráter "
        "individual ou coletivo, compreendendo práticas corporais, artísticas e culturais, práticas integrativas e complementares, atividades"
        "físicas, promoção da alimentação saudável ou educação em saúde."),
        ("17", "Imunização", "Conjunto de ações que objetivam a administração de vacinas para estimulação da resposta imune do hospedeiro, "
        "incluindo quaisquer preparações para a profilaxia imunológica ativa. Exige informação da Instalação Física — Sala de Vacina, o "
        "Atendimento Ambulatorial de Média Complexidade e o Serviço Especializado"),
        
    ]

    sus = [
        (1, "SIM"),
        (2, "NÃO")
    ]
    
    vinculo_profissional = [
        ("010101", "Estatutário Efetivo - Servidor Próprio", "Servidor da Administração Pública Direta ou Indireta, ocupante de cargo "
        "efetivo do próprio ente público regido pelo Regime Jurídico Único (federal, estadual e municipal) e militar, vinculado a "
        "Regime Próprio de Previdência ou ao Regime Geral de Previdência Social."),
        ("010102", "Estatutário Efetivo - Servidor Cedido", "Servidor da Administração Pública Direta ou Indireta ocupante de cargo"
        "efetivo, cedido por outro ente público, regido pelo Regime Jurídico Único (federal, estadual e municipal) e militar, vinculado"
        " a Regime Próprio de Previdência ou ao Regime Geral de Previdência Social."),
        ("010202", "Empregado Público Celetista - Empregado Próprio ", "Empregado público do próprio ente/entidade pública da Administração"
        "Pública Direta ou Indireta, ocupante de emprego público, contratado pelo, regime CLT por prazo indeterminado."),
        ("010203", "Empregado Público Celetista - Empregado Cedido", "Empregado público, cedido por outro ente/entidade pública da Administração"
        "Direta ou Indireta, ocupante de emprego público, contratado pela CLT por prazo indeterminado."),
        ("010301", "Contratado Temporário ou por Tempo Determinado - Servidor Publico", "Trabalhador temporário, contratado pela Administração" \
        " Pública Direta ou Indireta por prazo/tempo determinado, regido por lei específica (federal, estadual, distrital ou municipal) ou pela CLT."),
        ("010302", "Contratado Temporário ou por Tempo Determinado - Trabalhador Privado", "Trabalhador temporário, contratado por pessoa física ou" \
        " jurídica por prazo determinado, regido pela CLT."),
        ("010403", "Cargo Comissionado - Servidor Público Próprio", "Servidor ou empregado público efetivo, próprio do ente ou entidade pública"
        "da Administração Direta, ou Indireta, ocupante de cargos de livre nomeação e exoneração."),
        ("010404", "Cargo Comissionado - Servidor Público Cedido", "Servidor ou empregado público efetivo da Administração Pública Direta, ou "
        "Indireta, cedido por outro ente ou entidade pública, ocupante de cargos de livre nomeação e exoneração."),
        ("010405", "Cargo Comissionado - Sem vínculo com o setor publico", "Trabalhador não efetivo ocupante de cargos de livre nomeação e "
        "exoneração, sem vínculo com setor público."),
        ("010500",  "Celetista", "Trabalhador vinculado a empregador, pessoa jurídica de natureza privada ou pessoa física, por contrato de" \
        " trabalho regido pela CLT, por prazoindeterminado."),
        ("020900", "Pessoa Jurídica", "Trabalhador pessoa jurídica, sem vínculo empregatício com seu contratante, proprietário/sócio de" \
        " empresa privada."),
        ("021000", "Pessoa Física", "Trabalhador pessoa física, sem vínculo empregatício, contratado para prestação de apoio técnico/serviços " \
        "com objetivos específicos durante determinado prazo."),
        ("021100", "Cooperado", "Trabalhador associado à cooperativa, que presta serviços na rede própria da cooperativa, sem vínculo" \
        " empregatício."),
        ("050101", "Residente - Próprio", "Profissional cursando residência médica ou multiprofissional, caracterizada por treinamento em " \
        "serviço, com bolsa financiada pela instituição (pública ou privada) responsável pelo estabelecimento."),
        ("050102", "Residente - Subsidiado por outro Ente ou Entidade", "Profissional cursando residência médica ou multiprofissional, " \
        "caracterizada por treinamento em serviço, com bolsa subsidiada por outro ente/entidade."),
        ("060101", "Estagiário - Próprio", "Estudante de instituições de educação superior, educação profissional, ensino médio, da educação" \
        " especial e dos anos finais do ensino fundamental, desenvolvendo atividades curriculares obrigatórias ou não obrigatórias, em " \
        "ambiente de trabalho na modalidade profissional da educação de jovens e adultos. Pode ser remunerado, ou não, pela instituição "
        "(pública ou privada) responsável pelo estabelecimento. Regido pela Lei nº 11.788/2008."),
        ("060102", "Estagiário - Subsidiado por outro Ente ou Entidade", "Estudante de instituições de educação superior, educação profissional,"
        "ensino médio, da educação especial e dos anos finais do ensino fundamental, desenvolvendo atividades curriculares obrigatórias ou não" \
        " obrigatórias, em ambiente de trabalho na modalidade profissional da educação de jovens e adultos. Pode ser remunerado, ou não, por " \
        "outro ente/entidade (pública ou privada). Regido pela Lei nº 11.788/2008 (Lei do estágio)."),
        ("070101", "Bolsista - Próprio", "Profissional ou estudante que desenvolve atividades de ensino, pesquisa e extensão/ensino-serviço" \
        " financiada por instituição (pública ou privada) responsável pelo estabelecimento. Não regido pela Lei nº 11.788/2008 (Lei do estágio)."),
        ("070102", "Bolsista - Subsidiado por outro Ente ou Entidade", "Profissional ou estudante que desenvolve atividades de ensino, pesquisa e"
        "extensão/ensino-serviço financiada por outro ente/entidade (pública ou privada). Não regido pela Lei nº 11.788/2008 (Lei do estágio)."),
        ("080100", "Empregado Público Celetista", "Empregado público intermediado por ente/entidade pública, ocupante de emprego público," \
        " contratado pelo regime CLT por prazo indeterminado."),
        ("080200", "Contratado Temporário ou por Prazo Determinado", "Trabalhador temporário intermediado pela administração pública ou por"
        "pessoa física, ou pessoa jurídica por prazo determinado, regido por lei específica (ente público) ou pela CLT."),
        ("080300", "Cargo Comissionado", "Trabalhador sem vínculo ou servidor ou empregado público efetivo, ocupante de cargo de livre nomeação" \
        " e exoneração intermediadas por órgãos ou entidade da Administração Pública Direta ou Indireta."),
        ("080400", "Celetista", "Trabalhador intermediado vinculado a empregador, pessoa jurídica de natureza privada ou pessoa física, por " \
        "contrato de trabalho regido pela CLT, por prazo indeterminado."),
        ("080501", "Autônomo - Pessoa Jurídica", "Trabalhador pessoa jurídica, sem vínculo empregatício com o contratante intermediador," \
        " proprietário/sócio de empresa privada."),
        ("080502", "Autônomo - Pessoa Física", "Trabalhador pessoa física, sem vínculo empregatício com o intermediador, contratado para prestação" \
        " de apoio técnico/serviços com objetivos específicos durante determinado prazo"),
        ("080600", "Cooperado", "Trabalhador associado à cooperativa intermediadora que presta serviços na rede de saúde."),
        ("080700", "Servidor Público - Cedido", "Servidor da Administração Pública Direta ou Indireta ocupante de cargo efetivo, cedido por" \
        " outro ente público, regido pelo Regime Jurídico Único (federal, estadual e municipal) e militar, vinculado a Regime Próprio de " \
        "Previdência ou ao Regime Geral de Previdência Social."),
        ("090100", "Contratado Verbalmente", "Profissional sem contrato formal com o empregador, aguardando sua regularização (situação excepcional)."),
        ("090200", "Voluntariado", "Profissional sem contrato formal com o empregador que atue de forma gratuita."),
        ("100100", "Servidor Cedido", "Servidor da Administração Pública Direta ou Indireta, ocupante de cargo efetivo, cedido por ente público, " \
        "regido pelo Regime Jurídico Único (federal, estadual e municipal) e militar, vinculado a Regime Próprio de Previdência ou ao Regime Geral" \
        " de Previdência Social."),
        ("100200", "Empregado Público Celetista", "Empregado público, cedido por ente/entidade pública da Administração Direta ou Indireta, ocupante" \
        " de emprego público, contratado pela CLT por prazo indeterminado."),
        ("100300", "Cargo Comissionado", "Trabalhador sem vínculo ou servidor, ou empregado público efetivo, ocupante de cargo de livre nomeação e" \
        " exoneração intermediadas por órgãos ou entidade da Administração Pública Direta ou Indireta."),

    ]
    
    tipo_leito = [
        (1, "BUCO MAXILO FACIAL"),
        (2, "CARDIOLOGIA"),
        (3, "CIRURGIA GERAL"),
        (4, "ENDOCRINOLOGIA"),
        (5, "GASTROENTEROLOGIA"),
        (6, "GINECOLOGIA"),
        (7, "CIRÚRGICO/DIAGNOSTICO/TERAPÊUTICO"),
        (8, "NEFROLOGIAUROLOGIA"),
        (9, "NEUROCIRURGIA"),
        (10, "OBSTETRICIA CIRÚRGICA"),
        (11, "OFTALMOLOGIA"),
        (12, "ONCOLOGIA"),
        (13, "ORTOPEDIATRAUMATOLOGIA"),
        (14, "OTORRINOLARINGOLOGIA"),
        (15, "PLÁSTICA"),
        (16, "TORÁCICA"),
        (31, "AIDS"),
        (32, "CARDIOLOGIA"),
        (33, "CLINICA GERAL"),
        (34, "CRÔNICOS"),
        (35, "DERMATOLOGIA"),
        (36, "GERIATRIA"),
        (37, "HANSENOLOGIA"),
        (38, "HEMATOLOGIA"),
        (40, "NEFROUROLOGIA"),
        (41, "NEONATOLOGIA"),
        (42, "NEUROLOGIA"),
        (43, "OBSTETRÍCIA CLINICA"),
        (44, "ONCOLOGIA"),
        (45, "PEDIATRIA CLINICA"),
        (46, "PNEUMOLOGIA"),
        (47, "PSIQUIATRIA"),
        (48, "REABILITAÇÃO"),
        (49, "PNEUMOLOGIA SANITÁRIA"),
        (64, "UNIDADE INTERMEDIARIA"),
        (65, "UNIDADE INTERMEDIARIA NEONATAL"),
        (66, "UNIDADE ISOLAMENTO"),
        (67, "TRANSPLANTE"),
        (68, "PEDIATRIA CIRÚRGICA"),
        (69, "AIDS"),
        (70, "FIBROSE CÍSTICA"),
        (71, "INTERCORRÊNCIA PÓS-TRANSPLANTE"),
        (72, "GERIATRIA"),
        (73, "SAÚDE MENTAL"),
        (74, "UTI ADULTO - TIPO I"),
        (75, "UTI ADULTO - TIPO II"),
        (76, "UTI ADULTO - TIPO III"),
        (77, "UTI PEDIÁTRICA - TIPO I"),
        (78, "UTI PEDIÁTRICA - TIPO II"),
        (79, "UTI PEDIÁTRICA - TIPO III"),
        (80, "UTI NEONATAL - TIPO I"),
        (81, "UTI NEONATAL - TIPO II"),
        (82, "UTI NEONATAL - TIPO III"),
        (83, "UTI DE QUEIMADOS"),
        (84, "ACOLHIMENTO NOTURNO"),
        (85, "UTI CORONARIANA TIPO II — UCO TIPO II"),
        (86, "UTI CORONARIANA TIPO III — UCO TIPO III"),
        (87, "SAÚDE MENTAL (CLINICO)"),
        (88, "QUEIMADO ADULTO (CLINICO)"),
        (89, "QUEIMADO PEDIÁTRICO (CLINICO)"),
        (90, "QUEIMADO ADULTO (CIRÚRGICO)"),
        (91, "QUEIMADO PEDIÁTRICO (CIRÚRGICO)"),
        (92, "UNIDADE DE CUIDADOS INTERMEDIÁRIOS NEONATAL CONVENCIONAL"),
        (93, "UNIDADE DE CUIDADOS INTERMEDIÁRIOS NEONATAL CANGURU"),
        (94, "UNIDADE DE CUIDADOS INTERMEDIÁRIOS PEDIÁTRICO"),
        (95, "UNIDADE DE CUIDADOS INTERMEDIÁRIOS ADULTO")
        
    ]

    tipo_equipamento = [
        (1, "EQUIPAMENTOS DE DIAGNÓSTICO POR IMAGEM"),
        (2, "EQUIPAMENTOS DE INFRAESTRUTURA"),
        (3, "EQUIPAMENTOS POR MÉTODOS ÓPTICOS"),
        (4, "EQUIPAMENTOS POR MÉTODOS GRÁFICOS"),
        (5, "EQUIPAMENTOS PARA MANUTENÇÃO DA VIDA"),
        (6, "OUTROS EQUIPAMENTOS"),
        (7, "EQUIPAMENTOS DE ODONTOLOGIA"),
        (8, "EQUIPAMENTOS DE AUDIOLOGIA"),

    ]

    financiamento = [
        ("PAB", "Piso de Atenção Básica"),
        ("MAC", "Limite Financeiro de Média e Alta Complexidade Ambulatorial e Hospitalar"),
        ("FAEC", "Fundo de Ações Estratégicas e Compensação"),

    ]

    origem_informacoes = [
        ("BPA", "Sistemas de Informação de Saúde (SIS/SUS)"),
        ("PNI", "Programa Nacional de Imunizações"),
        ("SIE", "SIGAE"),
        ("SIB", "SIGAB"),
        ("MIN", "MATERNO INFANTIL"),
        ("PAC", "PROGRAMA AÇÃO COMUNITÁRIA"),
        ("SCL", "SISCOLO"),
        ("EXT", "OUTROS SISTEMAS"),

    ]

    identificacao_aih = [
        (1, "AIH Principal"),
        (3, "AIH de Continuação"),
        (5, "AIH de Longa Permanência"),
    ]

    modalidade_internacao = [
        (2, "Hospitalar"),
        (3, "Hospital Dia"),
        (4, "Internação Domiciliar")
    ]
    
    carater_internacao = [
        (1, "Eletiva"),
        (2, "Urgência/Emergência em Unidade de Referência"),
        (3, "Urgência/Emergência, quando a AIH tiver sido emitida antes da internação"),
        (4, "Internação em AIH de alta complexidade"),
        (5, "Urgência/Emergência, quando a AIH tiver sido emitida após a internação."),
        (6, "quadro compatível com acidente no local de trabalho ou a serviço da empresa"),
        (7, "quadro compatível com acidente de trajeto entre a residência e trabalho"),
        (8, "quadro compatível com outros tipos de acidente de trânsito, não considerados acidentes de trajeto entre residência e trabalho"),
        (9, "quadro compatível com outros tipos de lesões e envenenamentos, por agentes físicos ou químicos."),
        (11, "Eletiva - atendimento em regime de hospital-dia"),
        (20, "Urgência/Emergência em Unidade de Referência"),
        (21, "Urgência/Emergência em Unidade de Referência - atendimento em regime de hospital-dia"),
        (26, "Urgência/Emergência - quadro compatível com acidente no local de trabalho ou a serviço da empresa"),
        (27, "Urgência/Emergência - quadro compatível com acidente de trajeto entre a residência e trabalho"),
        (28, "Urgência/Emergência - quadro compatível com outros tipos de acidente de trânsito, não considerados acidentes de trajeto entre" \
        " residência e trabalho"),
        (29, "Urgência/Emergência - quadro compatível com outros tipos de lesões e envenenamentos, por agentes físicos ou químicos."),
        (41, "Internação em AIH de alta complexidade - atendimento em regime de hospital-dia"),

    ]
    
    
    motivo_saida = [
        ("1.1", "Alta Curado"),
        ("1.2", "Alta Melhorado"),
        ("1.3", "Alta da Puérpera e permanência do recém-nascido"),
        ("1.4", "Alta a pedido"),
        ("1.5", "Alta com previsão de retorno para acompanhamento do paciente"),
        ("1.6", "Alta por Evasão"),
        ("1.7", "Alta da Puérpera e recém-nascido"),
        ("1.8", "Alta por Outros motivos"),
        ("2.1", "Por características próprias da doença"),
        ("2.2", "Por Intercorrência"),
        ("2.3", "Por impossibilidade sócio-familiar"),
        ("2.4", "Por Processo de doação de órgãos, tecidos e células - doador vivo"),
        ("2.5", "Por Processo de doação de órgãos, tecidos e células - doador morto"),
        ("2.6", "Por mudança de Procedimento"),
        ("2.7", "Por reoperação"),
        ("2.8", "Outros motivos"),
        ("3.1", "Transferido para outro estabelecimento"),
        ("4.1", "Com declaração de óbito fornecida pelo médico assistente"),
        ("4.2", "Com declaração de Óbito fornecida pelo Instituto Médico Legal - IML"),
        ("4.3", "Com declaração de Óbito fornecida pelo Serviço de Verificação de Óbito - SVO"),
        ("5.1", "ENCERRAMENTO ADMINISTRATIVO")
    ]
    
    faixa_etaria = [
        (1, "Menor de 1 ano"),
        (2, "1 a 4 anos, 5 a 9 anos"),
        (3, "10 a 14 anos"),
        (4, "15 a 19 anos"),
        (5, "20 a 24 anos"),
        (6, "25 a 29 anos"),
        (7, "30 a 34 anos"),
        (8, "35 a 39 anos"),
        (9, "40 a 44 anos"),
        (10, "45 a 49 ano"),
        (11, "50 a 54 anos"),
        (12, "55 a 59 anos"),
        (13, "60 a 64 anos"),
        (14, "65 a 69 anos"),
        (15, "70 a 74 anos"),
        (16, "75 a 79 anos"),
        (17, "80 anos e mais e idade ignorada")
    ]
    
    raca_cor = [
        (1, "Branca"),
        (2, "Preta"),
        (3, "Parda"),
        (4, "Amarela"),
        (5, "Indígena"),
        (6, "Não informado"),
    ]

    gravidez_risco = [
        (1, "SIM"),
        (2, "NÃO")
    ]
    
    tipo_parto = [
        (1, "Vaginal"),
        (2, "Cesárea"),
        (3, "Ignorado")
    ]

    tempo_gestacao = [
        (1, "Antes de 37 semanas (parto prematuro)"),
        (2, "37 a 41 semanas"),
        (3, "42 semanas ou mais")
    ]
   
    tipo_vacina = [
        (1, "BCG"),
        (2, "Hepatite B"),
        (3, "Poliomielite 1, 2 e 3 (VIP)"),
        (4, "Poliomielite 1 e 3 (VOPb)"),
        (5, "Rotavírus humano G1P[8] (ROTA"),
        (6, "(DTP/HB/Hib) (Penta)"),
        (7, "Pneumocócica 10 (VPC 10 - conjugada)"),
        (8, "Meningocócica C"),
        (9, "Vacina COVID-19"),
        (10, "Febre Amarela"),
        (11, "Sarampo, caxumba, rubéola"),
        (12, "Hepatite A"),
        (13, "Difteria, Tétano e Pertussis (DTP)"),
        (14, "Difteria e Tétano (dT)"),
        (15, "HPV4"),
        (16, "VPP 23"),
        (17, "Varicela"),
    ]
    
    db.bulk_save_objects([ClassificacaoEstabelecimentoSaude(id=c, descricao=d) for c, d in tipo_estabelecimento])
    db.bulk_save_objects([AtividadeEstabelecimentoSaude(id=c, atividade=d, descricao=a) for c, d, a in atividade_estabelecimento])
    db.bulk_save_objects([Sus(id=c, descricao=d) for c, d in sus])
    db.bulk_save_objects([VinculoProfissional(id=c, FormaContratacao = a, descricao=d) for c, a, d in vinculo_profissional])
    db.bulk_save_objects([TiposLeito(id=c, descricao=d) for c, d in tipo_leito])
    db.bulk_save_objects([TipoEquipamento(id=c, descricao=d) for c, d in tipo_equipamento])
    db.bulk_save_objects([TipoFinanciamento(id=c, descricao=d) for c, d in financiamento])
    db.bulk_save_objects([OrigemInformacoes(id=c, descricao=d) for c, d in origem_informacoes])
    db.bulk_save_objects([IdentificacaoAIH(id=c, descricao=d) for c, d in identificacao_aih])
    db.bulk_save_objects([ModalidadeInternacao(id=c, descricao=d) for c, d in modalidade_internacao])
    db.bulk_save_objects([CaraterInternacao(id=c, descricao=d) for c, d in carater_internacao])
    db.bulk_save_objects([MotivoSaida(id=c, descricao=d) for c , d in motivo_saida])
    db.bulk_save_objects([FaixaEtaria(id=c, descricao=d) for c, d in faixa_etaria])
    db.bulk_save_objects([RacaCor(id=c, tipo=d) for c ,d in raca_cor])
    db.bulk_save_objects([GravidezRisco(id=c, descricao=d) for c ,d in gravidez_risco])
    db.bulk_save_objects([TipoParto(id=c, nome=d) for c ,d in tipo_parto])
    db.bulk_save_objects([TempoGestacao(id=c, nome=d) for c ,d in tempo_gestacao])
    db.bulk_save_objects([TipoVacina(id=c, nome=d) for c ,d in tipo_vacina])

    db.commit()
