"""
Módulo de funções auxiliares.
Contém funções reutilizáveis para validação, formatação e operações comuns.
"""

import re
from datetime import datetime
import streamlit as st


def validar_email(email: str) -> bool:
    """
    Valida se uma string é um email válido.
    
    Args:
        email (str): Email a ser validado
        
    Returns:
        bool: True se email é válido, False caso contrário
    """
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None


def validar_nome(nome: str) -> bool:
    """
    Valida se o nome contém apenas letras e espaços.
    
    Args:
        nome (str): Nome a ser validado
        
    Returns:
        bool: True se nome é válido, False caso contrário
    """
    if not nome or len(nome.strip()) < 3:
        return False
    return all(c.isalpha() or c.isspace() for c in nome)


def validar_leito(leito) -> bool:
    """
    Valida se o leito é válido.
    
    Args:
        leito: Leito (pode ser string do dropdown ou número)
        
    Returns:
        bool: True se leito é válido (não vazio), False caso contrário
    """
    if isinstance(leito, str):
        return len(leito.strip()) > 0
    elif isinstance(leito, (int, float)):
        return leito > 0
    return False


def formatar_data_br(data: datetime) -> str:
    """
    Formata uma data para o padrão brasileiro (DD/MM/YYYY HH:MM).
    
    Args:
        data (datetime): Data a ser formatada
        
    Returns:
        str: Data formatada no padrão brasileiro
    """
    return data.strftime("%d/%m/%Y %H:%M")


def formatar_data_sql(data: datetime) -> str:
    """
    Formata uma data para o padrão SQL (YYYY-MM-DD HH:MM:SS).
    
    Args:
        data (datetime): Data a ser formatada
        
    Returns:
        str: Data formatada no padrão SQL
    """
    return data.strftime("%Y-%m-%d %H:%M:%S")


def converter_data_br_para_sql(data_str: str) -> datetime:
    """
    Converte uma data no formato brasileiro (DD/MM/YYYY) para datetime.
    
    Args:
        data_str (str): Data em formato brasileiro
        
    Returns:
        datetime: Objeto datetime convertido
    """
    try:
        return datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError:
        return datetime.now()


def truncar_texto(texto: str, max_chars: int = 50) -> str:
    """
    Trunca um texto para um número máximo de caracteres.
    
    Args:
        texto (str): Texto a ser truncado
        max_chars (int): Número máximo de caracteres
        
    Returns:
        str: Texto truncado com "..." ao final se necessário
    """
    if len(texto) <= max_chars:
        return texto
    return texto[:max_chars-3] + "..."


def exibir_mensagem_sucesso(mensagem: str) -> None:
    """
    Exibe uma mensagem de sucesso visual ao usuário.
    
    Args:
        mensagem (str): Texto da mensagem
    """
    st.success(f"✓ {mensagem}")


def exibir_mensagem_erro(mensagem: str) -> None:
    """
    Exibe uma mensagem de erro visual ao usuário.
    
    Args:
        mensagem (str): Texto da mensagem
    """
    st.error(f"✗ {mensagem}")


def exibir_mensagem_aviso(mensagem: str) -> None:
    """
    Exibe uma mensagem de aviso visual ao usuário.
    
    Args:
        mensagem (str): Texto da mensagem
    """
    st.warning(f"⚠️ {mensagem}")


def exibir_mensagem_info(mensagem: str) -> None:
    """
    Exibe uma mensagem de informação visual ao usuário.
    
    Args:
        mensagem (str): Texto da mensagem
    """
    st.info(f"ℹ️ {mensagem}")


def obter_proxima_id() -> int:
    """
    Gera um novo ID único baseado no timestamp.
    
    Returns:
        int: ID único
    """
    return int(datetime.now().timestamp() * 1000)


def calcular_taxa_percentual(parte: int, total: int) -> float:
    """
    Calcula a taxa percentual entre dois números.
    
    Args:
        parte (int): Valor parcial
        total (int): Valor total
        
    Returns:
        float: Percentual calculado (0-100)
    """
    if total == 0:
        return 0.0
    return (parte / total) * 100


def formatar_percentual(valor: float) -> str:
    """
    Formata um valor numérico como percentual com 2 casas decimais.
    
    Args:
        valor (float): Valor numérico
        
    Returns:
        str: Percentual formatado (ex: "75.50%")
    """
    return f"{valor:.2f}%"


def obter_intervalo_datas_dinamico(tipo: str) -> tuple:
    """
    Retorna um intervalo de datas baseado no tipo especificado.
    
    Args:
        tipo (str): Tipo de intervalo ('hoje', 'semana', 'mes', 'ano')
        
    Returns:
        tuple: (data_inicio, data_fim) como objetos datetime
    """
    hoje = datetime.now()
    
    if tipo == 'hoje':
        return (hoje.replace(hour=0, minute=0, second=0, microsecond=0), hoje)
    elif tipo == 'semana':
        inicio = datetime(hoje.year, hoje.month, hoje.day - hoje.weekday())
        return (inicio, hoje)
    elif tipo == 'mes':
        inicio = datetime(hoje.year, hoje.month, 1)
        return (inicio, hoje)
    elif tipo == 'ano':
        inicio = datetime(hoje.year, 1, 1)
        return (inicio, hoje)
    else:
        return (hoje, hoje)
