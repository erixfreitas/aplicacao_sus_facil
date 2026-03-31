"""
Configurações de desenvolvimento e variáveis de ambiente.
Use este arquivo para customizações locais sem afetar o código principal.
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# ============================================================================
# AMBIENTE
# ============================================================================
AMBIENTE = os.getenv('AMBIENTE', 'desenvolvimento')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# ============================================================================
# CAMINHO DE ARQUIVOS
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATABASE_FILE = os.path.join(DATA_DIR, 'dados.csv')

# ============================================================================
# APLICAÇÃO
# ============================================================================
APP_NAME = "SUS Fácil"
APP_VERSION = "1.0.0"
AUTOR = "Equipe de Desenvolvimento"

# ============================================================================
# LOGGING
# ============================================================================
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.path.join(BASE_DIR, 'app.log')

# ============================================================================
# PAGINAÇÃO
# ============================================================================
ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', '10'))

# ============================================================================
# CACHE
# ============================================================================
ENABLE_CACHE = os.getenv('ENABLE_CACHE', 'True').lower() == 'true'
CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))  # 1 hora

# ============================================================================
# VALIDAÇÕES
# ============================================================================
MIN_NOME_LENGTH = 3
MAX_NOME_LENGTH = 100
MIN_LEITO = 1
MAX_LEITO = 999

# ============================================================================
# CORES E TEMA
# ============================================================================
THEME = os.getenv('THEME', 'light')  # light ou dark
PRIMARY_COLOR = os.getenv('PRIMARY_COLOR', '#1f77b4')

# ============================================================================
# FUNCIONALIDADES EXPERIMENTAIS
# ============================================================================
ENABLE_EXPERIMENTAL_FEATURES = DEBUG
ENABLE_PDF_EXPORT = False  # Será habilitado quando dependência for adicionada
ENABLE_EXCEL_EXPORT = False  # Será habilitado quando dependência for adicionada

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def criar_diretorios_necessarios():
    """Cria diretórios necessários se não existirem."""
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"✓ Diretório de dados criado: {DATA_DIR}")


def validar_ambiente():
    """Valida se o ambiente está configurado corretamente."""
    print(f"\n{'='*60}")
    print(f"Ambiente: {AMBIENTE}")
    print(f"Debug: {DEBUG}")
    print(f"Versão: {APP_VERSION}")
    print(f"Base Dir: {BASE_DIR}")
    print(f"Data Dir: {DATA_DIR}")
    print(f"{'='*60}\n")


# Executar ao importar
if __name__ == "__main__":
    criar_diretorios_necessarios()
    validar_ambiente()
