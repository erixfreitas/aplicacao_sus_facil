"""
Módulo de constantes e configurações globais da aplicação.
Define dados estáticos como listas de opções para dropdowns e configurações gerais.
"""

# ============================================================================
# CONFIGURAÇÕES GERAIS
# ============================================================================
APP_TITLE = "Sistema de Solicitações Hospitalares"
APP_ICON = "🏥"
THEME_COLOR = "#1f77b4"
SIDEBAR_ICON = "⚙️"

# ============================================================================
# BANCO DE DADOS
# ============================================================================
DATABASE_FILE = "data/dados.csv"
CSV_COLUMNS = [
    "id",
    "data",
    "nome_paciente",
    "cidade",
    "hospital",
    "solicitante",
    "diagnostico",
    "leito_solicitado",
    "especialidade",
    "aceito",
    "nome_medico",
    "nome_recepcionista",
    "codigo_justificativa",
    "data_criacao",
    "data_atualizacao"
]

# ============================================================================
# OPÇÕES PARA DROPDOWNS
# ============================================================================
CIDADES = [
    "Brasópolis",
    "Cachoeira de Minas",
    "Conceição das Pedras",
    "Conceição dos Ouros",
    "Cristina",
    "Delfim Moreira",
    "Gonçalves",
    "Itajubá",
    "Maria da Fé",
    "Marmelópolis",
    "Paraisópolis",
    "Pedralva",
    "Piranguçu",
    "Piranguinho",
    "Santa Rita do Sapucaí",
    "São José do Alegre",
    "Sapucaí-Mirim",
    "Wenceslau Braz",
    "Outros"
]

LEITOS = [
    "UCCI",
    "Saúde Mental",
    "Pediatria",
    "Clínico Geral",
    "Cirúrgia Geral",
    "Neurologia",
    "Cardiologia",
    "Obstetrícia",
    "Ginecologia",
    "Nefrologia",
    "Ortopedia",
    "Traumatologia"
]

MEDICOS = [
    "Roger Souza",
    "Gustavo Martins",
    "Alessandra Rabelo",
    "Zuleica Gonzaga",
    "Raimundo Silva"
]

RECEPCIONISTAS = [
    "Ana Gabriela Costa",
    "Daniele Aparecida da Silva",
    "Joyce Cristiellen Campos Vieira",
    "Aléxia Adryane Sales Dias",
    "Karoline Aparecida dos Santos",
    "Maria José Ramos de Oliveira",
    "Gabrine Larissa Ferreira da Silva",
    "Luana Maria Custódio",
    "Maysa Silva Ferreira Eduardo",
    "Natália Alves",
    "Renilda Maria da Silva Martins",
    "Rosana Aparecida Rodrigues",
    "Tatiane Akemi Faria Kishi",
    "Matheus Nascimento Giffoni",
    "Luciana Aparecida de Lima"
]

# Preenchimento aberto para Hospital - usuário digita o nome
HOSPITAIS = []

# Preenchimento aberto para Diagnóstico - usuário digita o diagnóstico
DIAGNOSTICOS = []

# Preenchimento aberto para Especialidade - usuário digita a especialidade
ESPECIALIDADES = []

CODIGOS_JUSTIFICATIVA = {
    "001": "Falta de Leito Normal",
    "002": "Falta de Leito de UTI",
    "003": "Falta de Leito de Isolamento",
    "005": "Falta de Especialidade Médica",
    "006": "Hospital de Referência",
    "007": "Leito Feminino/Masculino",
    "008": "Incoerência de Dados/Pendência de Exames",
    "009": "Direcionar o Laudo Mais Tarde",
    "010": "Sem Critérios para Leito de UCCI",
    "011": "Falta de Leito de UCCI",
    "012": "Necessidade de Especialistas Fora da Complexidade UCCI",
    "013": "Diagnóstico Não Condizente com a Clínica UCCI"
}

# ============================================================================
# CONFIGURAÇÕES DE FILTROS
# ============================================================================
FILTROS_PADROES = {
    "data_inicio": None,
    "data_fim": None,
    "nome_paciente": "",
    "hospital": None,
    "especialidade": None,
    "status": None  # None = todos, True = Aceito, False = Não Aceito
}

# ============================================================================
# ESTILOS E CORES
# ============================================================================
COR_SUCESSO = "#00cc66"
COR_ERRO = "#ff4444"
COR_AVISO = "#ffaa00"
COR_INFORMACAO = "#1f77b4"

# Paleta de cores para gráficos
CORES_GRAFICO = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]

# ============================================================================
# CONFIGURAÇÕES DE PAGINAÇÃO
# ============================================================================
LINHAS_POR_PAGINA = 10
LINHAS_TABELA_INDICADORES = 5
