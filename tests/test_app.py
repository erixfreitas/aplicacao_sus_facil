"""
Script de teste para validar que todos os módulos estão funcionando corretamente.
Execute: python test_app.py
"""

import sys
import os
from datetime import datetime

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def teste_imports():
    """Testa se todos os módulos podem ser importados."""
    print("\n🧪 Testando importações...")
    
    try:
        from utils.constants import CIDADES, DIAGNOSTICOS
        print("  ✓ utils.constants")
    except Exception as e:
        print(f"  ✗ utils.constants: {e}")
        return False
    
    try:
        from utils.helpers import validar_nome, formatar_data_br
        print("  ✓ utils.helpers")
    except Exception as e:
        print(f"  ✗ utils.helpers: {e}")
        return False
    
    try:
        from modules.database import GerenciadorDados
        print("  ✓ modules.database")
    except Exception as e:
        print(f"  ✗ modules.database: {e}")
        return False
    
    try:
        from modules.filters import FiltrosAvancados
        print("  ✓ modules.filters")
    except Exception as e:
        print(f"  ✗ modules.filters: {e}")
        return False
    
    try:
        from modules.charts import GeradorGraficos
        print("  ✓ modules.charts")
    except Exception as e:
        print(f"  ✗ modules.charts: {e}")
        return False
    
    return True


def teste_validacoes():
    """Testa funções de validação."""
    print("\n🧪 Testando validações...")
    
    from utils.helpers import validar_nome, validar_leito, validar_email
    
    # Teste validar_nome
    assert validar_nome("João Silva") == True, "Deve aceitar nome válido"
    assert validar_nome("Jo") == False, "Deve rejeitar nome curto"
    assert validar_nome("João123") == False, "Deve rejeitar nome com números"
    print("  ✓ validar_nome")
    
    # Teste validar_leito
    assert validar_leito(5) == True, "Deve aceitar leito válido"
    assert validar_leito(0) == False, "Deve rejeitar leito zero"
    assert validar_leito(-1) == False, "Deve rejeitar leito negativo"
    print("  ✓ validar_leito")
    
    # Teste validar_email
    assert validar_email("test@email.com") == True, "Deve aceitar email válido"
    assert validar_email("invalid-email") == False, "Deve rejeitar email inválido"
    print("  ✓ validar_email")
    
    return True


def teste_database():
    """Testa operações de banco de dados."""
    print("\n🧪 Testando banco de dados...")
    
    from modules.database import GerenciadorDados
    from datetime import datetime
    
    gerenciador = GerenciadorDados()
    
    # Teste: obter estatísticas (mesmo sem dados)
    stats = gerenciador.obter_estatisticas()
    assert 'total_solicitacoes' in stats, "Stats deve conter total_solicitacoes"
    print("  ✓ obter_estatisticas")
    
    # Teste: obter todas solicitações
    df = gerenciador.obter_todas_solicitacoes()
    assert df is not None, "Deve retornar DataFrame"
    print("  ✓ obter_todas_solicitacoes")
    
    return True


def teste_filtros():
    """Testa funcionalidades de filtro."""
    print("\n🧪 Testando filtros...")
    
    import pandas as pd
    from modules.filters import FiltrosAvancados
    
    # Criar DataFrame de teste
    df_teste = pd.DataFrame({
        'data': ['2025-01-01', '2025-01-02'],
        'nome_paciente': ['João', 'Maria'],
        'hospital': ['Hospital A', 'Hospital B'],
        'especialidade': ['Cardiologia', 'Neurologia'],
        'aceito': [True, False]
    })
    
    # Teste filtro por nome
    resultado = FiltrosAvancados.filtrar_por_nome_paciente(df_teste, 'João')
    assert len(resultado) == 1, "Deve encontrar João"
    print("  ✓ filtrar_por_nome_paciente")
    
    # Teste filtro por hospital
    resultado = FiltrosAvancados.filtrar_por_hospital(df_teste, 'Hospital A')
    assert len(resultado) == 1, "Deve encontrar Hospital A"
    print("  ✓ filtrar_por_hospital")
    
    # Teste filtro por status
    resultado = FiltrosAvancados.filtrar_por_status(df_teste, True)
    assert len(resultado) == 1, "Deve encontrar 1 aceita"
    print("  ✓ filtrar_por_status")
    
    return True


def teste_formatacao():
    """Testa funções de formatação."""
    print("\n🧪 Testando formatações...")
    
    from utils.helpers import (
        formatar_data_br, formatar_data_sql, 
        calcular_taxa_percentual, formatar_percentual
    )
    
    data = datetime(2025, 12, 26, 10, 30, 0)
    
    # Teste formatar_data_br
    resultado = formatar_data_br(data)
    assert "26/12/2025" in resultado, "Deve estar em formato brasileiro"
    print("  ✓ formatar_data_br")
    
    # Teste formatar_data_sql
    resultado = formatar_data_sql(data)
    assert "2025-12-26" in resultado, "Deve estar em formato SQL"
    print("  ✓ formatar_data_sql")
    
    # Teste calcular_taxa_percentual
    taxa = calcular_taxa_percentual(75, 100)
    assert taxa == 75.0, "Deve calcular 75%"
    print("  ✓ calcular_taxa_percentual")
    
    # Teste formatar_percentual
    resultado = formatar_percentual(75.5)
    assert "75.50%" in resultado, "Deve formatar corretamente"
    print("  ✓ formatar_percentual")
    
    return True


def teste_estrutura_pastas():
    """Testa se a estrutura de pastas está correta."""
    print("\n🧪 Testando estrutura de pastas...")
    
    pastas = [
        'pages',
        'modules', 
        'utils',
        'data'
    ]
    
    for pasta in pastas:
        caminho = os.path.join(os.path.dirname(__file__), pasta)
        assert os.path.isdir(caminho), f"Pasta {pasta} não encontrada"
        print(f"  ✓ {pasta}/")
    
    # Testar arquivos essenciais
    arquivos = [
        'app.py',
        'requirements.txt',
        'README.md',
        'pages/home.py',
        'pages/indicadores.py',
        'modules/database.py',
        'modules/charts.py',
        'modules/filters.py',
        'utils/constants.py',
        'utils/helpers.py'
    ]
    
    for arquivo in arquivos:
        caminho = os.path.join(os.path.dirname(__file__), arquivo)
        assert os.path.isfile(caminho), f"Arquivo {arquivo} não encontrado"
        print(f"  ✓ {arquivo}")
    
    return True


def main():
    """Executa todos os testes."""
    print("\n" + "="*60)
    print("🏥 SUS FÁCIL - TESTES DE VALIDAÇÃO")
    print("="*60)
    
    testes = [
        ("Estrutura de Pastas", teste_estrutura_pastas),
        ("Importações", teste_imports),
        ("Validações", teste_validacoes),
        ("Banco de Dados", teste_database),
        ("Filtros", teste_filtros),
        ("Formatação", teste_formatacao),
    ]
    
    resultados = []
    
    for nome, funcao_teste in testes:
        try:
            sucesso = funcao_teste()
            resultados.append((nome, sucesso))
        except Exception as e:
            print(f"  ✗ Erro: {e}")
            resultados.append((nome, False))
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    total = len(resultados)
    sucesso = sum(1 for _, s in resultados if s)
    falha = total - sucesso
    
    for nome, resultado in resultados:
        status = "✓ PASSOU" if resultado else "✗ FALHOU"
        print(f"{nome:.<40} {status}")
    
    print("-"*60)
    print(f"Total: {total} | Sucesso: {sucesso} | Falha: {falha}")
    
    if falha == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("\nVocê pode executar a aplicação com:")
        print("  streamlit run app.py")
        return 0
    else:
        print(f"\n❌ {falha} teste(s) falharam!")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
