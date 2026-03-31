"""
Módulo de gerenciamento de banco de dados.
Realiza operações de CRUD (Create, Read, Update, Delete) com persistência em CSV.
"""

import pandas as pd
from datetime import datetime
import os
from typing import List, Dict, Optional
import streamlit as st

from utils.constants import (
    DATABASE_FILE, CSV_COLUMNS, CIDADES, HOSPITAIS, 
    DIAGNOSTICOS, ESPECIALIDADES, CODIGOS_JUSTIFICATIVA
)
from utils.helpers import (
    obter_proxima_id, formatar_data_sql, validar_nome, 
    validar_leito, exibir_mensagem_erro, exibir_mensagem_sucesso
)


class GerenciadorDados:
    """
    Classe responsável por todas as operações com dados (CRUD).
    Utiliza CSV para persistência de dados.
    """
    
    def __init__(self):
        """Inicializa o gerenciador de dados e cria arquivo CSV se não existir."""
        self.arquivo = DATABASE_FILE
        self._criar_arquivo_se_nao_existe()
    
    def _criar_arquivo_se_nao_existe(self) -> None:
        """Cria o arquivo CSV com colunas vazias se não existir."""
        if not os.path.exists(self.arquivo):
            os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
            df = pd.DataFrame(columns=CSV_COLUMNS)
            df.to_csv(self.arquivo, index=False, encoding='utf-8')
    
    def _carregar_dados(self) -> pd.DataFrame:
        """
        Carrega todos os dados do arquivo CSV.
        
        Returns:
            pd.DataFrame: DataFrame com os dados do CSV
        """
        try:
            df = pd.read_csv(self.arquivo, encoding='utf-8')
            # Garantir que todas as colunas existem
            for col in CSV_COLUMNS:
                if col not in df.columns:
                    df[col] = None
            return df[CSV_COLUMNS]
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")
            return pd.DataFrame(columns=CSV_COLUMNS)
    
    def _salvar_dados(self, df: pd.DataFrame) -> bool:
        """
        Salva os dados no arquivo CSV.
        
        Args:
            df (pd.DataFrame): DataFrame a ser salvo
            
        Returns:
            bool: True se salvo com sucesso, False caso contrário
        """
        try:
            df[CSV_COLUMNS].to_csv(self.arquivo, index=False, encoding='utf-8')
            return True
        except Exception as e:
            st.error(f"Erro ao salvar dados: {str(e)}")
            return False
    
    def inserir_solicitacao(self, dados: Dict) -> bool:
        """
        Insere uma nova solicitação de internação.
        
        Args:
            dados (Dict): Dicionário com os dados da solicitação
            
        Returns:
            bool: True se inserido com sucesso, False caso contrário
        """
        # Validações
        if not validar_nome(dados.get('nome_paciente', '')):
            exibir_mensagem_erro("Nome do paciente inválido (mínimo 3 caracteres, apenas letras)")
            return False
        
        if not validar_leito(dados.get('leito_solicitado', '')):
            exibir_mensagem_erro("Leito solicitado é obrigatório")
            return False
        
        # Carregar dados existentes
        df = self._carregar_dados()
        
        # Criar novo registro
        novo_id = obter_proxima_id()
        agora = formatar_data_sql(datetime.now())
        
        novo_registro = {
            'id': novo_id,
            'data': dados.get('data', formatar_data_sql(datetime.now())),
            'nome_paciente': dados.get('nome_paciente', '').strip(),
            'cidade': dados.get('cidade', ''),
            'hospital': dados.get('hospital', ''),
            'solicitante': dados.get('solicitante', '').strip(),
            'diagnostico': dados.get('diagnostico', ''),
            'leito_solicitado': str(dados.get('leito_solicitado', '')),
            'especialidade': dados.get('especialidade', ''),
            'aceito': dados.get('aceito', False),
            'nome_medico': dados.get('nome_medico', '').strip(),
            'nome_recepcionista': dados.get('nome_recepcionista', '').strip(),
            'codigo_justificativa': dados.get('codigo_justificativa', ''),
            'data_criacao': agora,
            'data_atualizacao': agora
        }
        
        # Adicionar novo registro ao DataFrame
        df = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
        
        # Salvar
        if self._salvar_dados(df):
            exibir_mensagem_sucesso("Solicitação registrada com sucesso!")
            return True
        else:
            return False
    
    def obter_todas_solicitacoes(self) -> pd.DataFrame:
        """
        Obtém todas as solicitações registradas.
        
        Returns:
            pd.DataFrame: DataFrame com todas as solicitações
        """
        df = self._carregar_dados()
        if not df.empty:
            df['data'] = pd.to_datetime(df['data'], errors='coerce')
            df = df.sort_values('data', ascending=False)
        return df
    
    def obter_solicitacao_por_id(self, solicitacao_id: int) -> Optional[Dict]:
        """
        Obtém uma solicitação específica pelo ID.
        
        Args:
            solicitacao_id (int): ID da solicitação
            
        Returns:
            Optional[Dict]: Dicionário com dados da solicitação ou None
        """
        df = self._carregar_dados()
        resultado = df[df['id'] == solicitacao_id]
        
        if not resultado.empty:
            return resultado.iloc[0].to_dict()
        return None
    
    def atualizar_solicitacao(self, solicitacao_id: int, dados: Dict) -> bool:
        """
        Atualiza uma solicitação existente.
        
        Args:
            solicitacao_id (int): ID da solicitação
            dados (Dict): Dicionário com dados atualizados
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        df = self._carregar_dados()
        
        if solicitacao_id not in df['id'].values:
            exibir_mensagem_erro("Solicitação não encontrada")
            return False
        
        # Validações
        if 'nome_paciente' in dados and not validar_nome(dados.get('nome_paciente', '')):
            exibir_mensagem_erro("Nome do paciente inválido")
            return False
        
        # Atualizar registro
        indice = df[df['id'] == solicitacao_id].index[0]
        
        dados['data_atualizacao'] = formatar_data_sql(datetime.now())
        
        for chave, valor in dados.items():
            if chave in df.columns:
                df.at[indice, chave] = valor
        
        # Salvar
        if self._salvar_dados(df):
            exibir_mensagem_sucesso("Solicitação atualizada com sucesso!")
            return True
        else:
            return False
    
    def deletar_solicitacao(self, solicitacao_id: int) -> bool:
        """
        Deleta uma solicitação pelo ID.
        
        Args:
            solicitacao_id (int): ID da solicitação
            
        Returns:
            bool: True se deletado com sucesso, False caso contrário
        """
        df = self._carregar_dados()
        
        if solicitacao_id not in df['id'].values:
            exibir_mensagem_erro("Solicitação não encontrada")
            return False
        
        # Remover registro
        df = df[df['id'] != solicitacao_id]
        
        # Salvar
        if self._salvar_dados(df):
            exibir_mensagem_sucesso("Solicitação deletada com sucesso!")
            return True
        else:
            return False
    
    def duplicar_solicitacao(self, solicitacao_id: int) -> bool:
        """
        Cria uma cópia de uma solicitação existente.
        
        Args:
            solicitacao_id (int): ID da solicitação a duplicar
            
        Returns:
            bool: True se duplicado com sucesso, False caso contrário
        """
        solicitacao = self.obter_solicitacao_por_id(solicitacao_id)
        
        if not solicitacao:
            exibir_mensagem_erro("Solicitação não encontrada")
            return False
        
        # Remover ID para criar novo registro
        solicitacao.pop('id', None)
        solicitacao.pop('data_criacao', None)
        solicitacao.pop('data_atualizacao', None)
        
        # Inserir como nova solicitação
        return self.inserir_solicitacao(solicitacao)
    
    def obter_estatisticas(self) -> Dict:
        """
        Calcula estatísticas gerais dos dados.
        
        Returns:
            Dict: Dicionário com estatísticas
        """
        df = self._carregar_dados()
        
        if df.empty:
            return {
                'total_solicitacoes': 0,
                'total_aceitas': 0,
                'total_recusadas': 0,
                'taxa_aceitacao': 0.0,
                'cidade_mais_solicitada': 'N/A',
                'hospital_mais_ativo': 'N/A'
            }
        
        total = len(df)
        aceitas = df['aceito'].sum() if df['aceito'].dtype == bool else len(df[df['aceito'] == True])
        recusadas = total - aceitas
        taxa_aceitacao = (aceitas / total * 100) if total > 0 else 0
        
        hospital_mais_ativo = df['hospital'].mode()[0] if not df['hospital'].empty else 'N/A'
        cidade_mais_solicitada = df['cidade'].mode()[0] if not df['cidade'].empty else 'N/A'

        return {
            'total_solicitacoes': total,
            'total_aceitas': int(aceitas),
            'total_recusadas': int(recusadas),
            'taxa_aceitacao': round(taxa_aceitacao, 2),
            'cidade_mais_solicitada': cidade_mais_solicitada,
            'hospital_mais_ativo': hospital_mais_ativo
        }
    
    def exportar_csv(self, filtrado: bool = False, df_filtrado: Optional[pd.DataFrame] = None) -> bytes:
        """
        Exporta os dados para formato CSV.
        
        Args:
            filtrado (bool): Se deve exportar apenas dados filtrados
            df_filtrado (Optional[pd.DataFrame]): DataFrame filtrado para exportar
            
        Returns:
            bytes: Arquivo CSV em bytes
        """
        if filtrado and df_filtrado is not None:
            df = df_filtrado
        else:
            df = self._carregar_dados()
        
        return df.to_csv(index=False, encoding='utf-8').encode('utf-8')
    
    def obter_backup(self) -> str:
        """
        Cria um backup dos dados em arquivo com timestamp.
        
        Returns:
            str: Caminho do arquivo de backup criado
        """
        df = self._carregar_dados()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"data/backup_dados_{timestamp}.csv"
        
        os.makedirs("data", exist_ok=True)
        df.to_csv(backup_file, index=False, encoding='utf-8')
        
        return backup_file
