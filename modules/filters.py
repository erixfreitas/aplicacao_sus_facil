"""
Módulo de filtros e buscas.
Implementa lógica de filtragem e busca em dados de solicitações.
"""

import pandas as pd
from datetime import datetime
from typing import Optional, Dict, List


class FiltrosAvancados:
    """
    Classe responsável por aplicar filtros e buscas nos dados.
    """
    
    @staticmethod
    def filtrar_por_data(df: pd.DataFrame, data_inicio: Optional[datetime], 
                        data_fim: Optional[datetime]) -> pd.DataFrame:
        """
        Filtra solicitações por intervalo de datas.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            data_inicio (Optional[datetime]): Data inicial do filtro
            data_fim (Optional[datetime]): Data final do filtro
            
        Returns:
            pd.DataFrame: DataFrame filtrado
        """
        if df.empty:
            return df
        
        df_temp = df.copy()
        df_temp['data'] = pd.to_datetime(df_temp['data'], errors='coerce')
        
        if data_inicio:
            df_temp = df_temp[df_temp['data'] >= pd.Timestamp(data_inicio)]
        
        if data_fim:
            # Adicionar um dia para incluir até o final do dia especificado
            data_fim_ajustada = pd.Timestamp(data_fim) + pd.Timedelta(days=1)
            df_temp = df_temp[df_temp['data'] < data_fim_ajustada]
        
        return df_temp
    
    @staticmethod
    def filtrar_por_nome_paciente(df: pd.DataFrame, nome: str) -> pd.DataFrame:
        """
        Filtra solicitações por nome do paciente (busca parcial).
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            nome (str): Nome ou parte do nome a buscar
            
        Returns:
            pd.DataFrame: DataFrame filtrado
        """
        if df.empty or not nome:
            return df
        
        return df[df['nome_paciente'].str.contains(nome, case=False, na=False)]
    
    @staticmethod
    def filtrar_por_hospital(df: pd.DataFrame, hospital: Optional[str]) -> pd.DataFrame:
        """
        Filtra solicitações por hospital.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            hospital (Optional[str]): Nome do hospital
            
        Returns:
            pd.DataFrame: DataFrame filtrado
        """
        if df.empty or not hospital:
            return df
        
        return df[df['hospital'] == hospital]
    
    @staticmethod
    def filtrar_por_especialidade(df: pd.DataFrame, especialidade: Optional[str]) -> pd.DataFrame:
        """
        Filtra solicitações por especialidade.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            especialidade (Optional[str]): Nome da especialidade
            
        Returns:
            pd.DataFrame: DataFrame filtrado
        """
        if df.empty or not especialidade:
            return df
        
        return df[df['especialidade'] == especialidade]
    
    @staticmethod
    def filtrar_por_status(df: pd.DataFrame, status: Optional[bool]) -> pd.DataFrame:
        """
        Filtra solicitações por status de aceitação.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            status (Optional[bool]): True para aceitas, False para recusadas, None para todas
            
        Returns:
            pd.DataFrame: DataFrame filtrado
        """
        if df.empty or status is None:
            return df
        
        return df[df['aceito'] == status]
    
    @staticmethod
    def filtrar_por_cidade(df: pd.DataFrame, cidade: Optional[str]) -> pd.DataFrame:
        """
        Filtra solicitações por cidade.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            cidade (Optional[str]): Nome da cidade
            
        Returns:
            pd.DataFrame: DataFrame filtrado
        """
        if df.empty or not cidade:
            return df
        
        return df[df['cidade'] == cidade]
    
    @staticmethod
    def filtrar_por_diagnostico(df: pd.DataFrame, diagnostico: Optional[str]) -> pd.DataFrame:
        """
        Filtra solicitações por diagnóstico.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            diagnostico (Optional[str]): Nome do diagnóstico
            
        Returns:
            pd.DataFrame: DataFrame filtrado
        """
        if df.empty or not diagnostico:
            return df
        
        return df[df['diagnostico'] == diagnostico]
    
    @staticmethod
    def busca_livre(df: pd.DataFrame, termo: str) -> pd.DataFrame:
        """
        Realiza busca livre em múltiplos campos.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            termo (str): Termo a buscar
            
        Returns:
            pd.DataFrame: DataFrame filtrado
        """
        if df.empty or not termo:
            return df
        
        termo_lower = termo.lower()
        
        # Buscar em múltiplas colunas
        mascaras = [
            df['nome_paciente'].str.contains(termo_lower, case=False, na=False),
            df['hospital'].str.contains(termo_lower, case=False, na=False),
            df['cidade'].str.contains(termo_lower, case=False, na=False),
            df['nome_medico'].str.contains(termo_lower, case=False, na=False),
            df['diagnostico'].str.contains(termo_lower, case=False, na=False),
        ]
        
        # Combinar com OR
        mascara_final = mascaras[0]
        for mascara in mascaras[1:]:
            mascara_final = mascara_final | mascara
        
        return df[mascara_final]
    
    @staticmethod
    def aplicar_filtros_multiplos(df: pd.DataFrame, filtros: Dict) -> pd.DataFrame:
        """
        Aplica múltiplos filtros ao DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            filtros (Dict): Dicionário com os filtros a aplicar
                {
                    'data_inicio': datetime,
                    'data_fim': datetime,
                    'nome_paciente': str,
                    'hospital': str,
                    'especialidade': str,
                    'status': bool,
                    'cidade': str,
                    'diagnostico': str,
                    'busca_livre': str
                }
            
        Returns:
            pd.DataFrame: DataFrame filtrado
        """
        df_filtrado = df.copy()
        
        if filtros.get('data_inicio') or filtros.get('data_fim'):
            df_filtrado = FiltrosAvancados.filtrar_por_data(
                df_filtrado,
                filtros.get('data_inicio'),
                filtros.get('data_fim')
            )
        
        if filtros.get('nome_paciente'):
            df_filtrado = FiltrosAvancados.filtrar_por_nome_paciente(
                df_filtrado,
                filtros.get('nome_paciente')
            )
        
        if filtros.get('hospital'):
            df_filtrado = FiltrosAvancados.filtrar_por_hospital(
                df_filtrado,
                filtros.get('hospital')
            )
        
        if filtros.get('especialidade'):
            df_filtrado = FiltrosAvancados.filtrar_por_especialidade(
                df_filtrado,
                filtros.get('especialidade')
            )
        
        if filtros.get('status') is not None:
            df_filtrado = FiltrosAvancados.filtrar_por_status(
                df_filtrado,
                filtros.get('status')
            )
        
        if filtros.get('cidade'):
            df_filtrado = FiltrosAvancados.filtrar_por_cidade(
                df_filtrado,
                filtros.get('cidade')
            )
        
        if filtros.get('diagnostico'):
            df_filtrado = FiltrosAvancados.filtrar_por_diagnostico(
                df_filtrado,
                filtros.get('diagnostico')
            )
        
        if filtros.get('busca_livre'):
            df_filtrado = FiltrosAvancados.busca_livre(
                df_filtrado,
                filtros.get('busca_livre')
            )
        
        return df_filtrado
    
    @staticmethod
    def ordenar_dados(df: pd.DataFrame, coluna: str, decrescente: bool = True) -> pd.DataFrame:
        """
        Ordena o DataFrame por uma coluna.
        
        Args:
            df (pd.DataFrame): DataFrame a ordenar
            coluna (str): Nome da coluna para ordenação
            decrescente (bool): Se True, ordena de forma decrescente
            
        Returns:
            pd.DataFrame: DataFrame ordenado
        """
        if df.empty or coluna not in df.columns:
            return df
        
        return df.sort_values(by=coluna, ascending=not decrescente)
