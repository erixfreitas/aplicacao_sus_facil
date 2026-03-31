"""
Módulo de geração de gráficos e visualizações.
Cria gráficos usando Plotly para dashboard e análises.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional
from utils.constants import CORES_GRAFICO


class GeradorGraficos:
    """
    Classe responsável pela geração de gráficos e visualizações.
    """
    
    @staticmethod
    def grafico_barras_solicitacoes_por_periodo(df: pd.DataFrame, periodo: str = 'dia') -> go.Figure:
        """
        Gera gráfico de barras com solicitações por período.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            periodo (str): Período para agrupamento ('dia', 'semana', 'mes', 'ano')
            
        Returns:
            go.Figure: Gráfico Plotly
        """
        if df.empty:
            return _criar_grafico_vazio("Sem dados para exibir")
        
        df_temp = df.copy()
        df_temp['data'] = pd.to_datetime(df_temp['data'], errors='coerce')
        
        if periodo == 'dia':
            df_temp['periodo'] = df_temp['data'].dt.date
            labels_formato = None
        elif periodo == 'semana':
            df_temp['periodo'] = df_temp['data'].dt.isocalendar().week
            labels_formato = None
        elif periodo == 'mes':
            df_temp['periodo'] = df_temp['data'].dt.to_period('M')
            labels_formato = 'mes_abreviado'
        else:  # ano
            df_temp['periodo'] = df_temp['data'].dt.year
            labels_formato = None
        
        contagem = df_temp.groupby('periodo').size().reset_index(name='quantidade')
        
        # Formatar labels para mês abreviado
        if labels_formato == 'mes_abreviado':
            meses_abrev = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                          'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            labels_x = []
            for periodo_val in contagem['periodo']:
                month = periodo_val.month
                labels_x.append(meses_abrev[month - 1])
            x_data = labels_x
        else:
            x_data = contagem['periodo'].astype(str)
        
        fig = go.Figure(data=[
            go.Bar(
                x=x_data,
                y=contagem['quantidade'],
                marker=dict(color=CORES_GRAFICO[0]),
                text=contagem['quantidade'],
                textposition='auto'
            )
        ])
        
        max_valor = contagem['quantidade'].max()
        fig.update_layout(
            title="Solicitações por Período",
            xaxis_title="Período",
            yaxis_title="Quantidade",
            yaxis=dict(range=[0, max_valor * 1.5]),
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    @staticmethod
    def grafico_pizza_taxa_aceitacao(df: pd.DataFrame) -> go.Figure:
        """
        Gera gráfico de pizza mostrando taxa de aceitação.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            
        Returns:
            go.Figure: Gráfico Plotly
        """
        if df.empty:
            return _criar_grafico_vazio("Sem dados para exibir")
        
        aceitas = df['aceito'].sum() if df['aceito'].dtype == bool else len(df[df['aceito'] == True])
        recusadas = len(df) - aceitas
        
        labels = ['Aceitas', 'Recusadas']
        valores = [aceitas, recusadas]
        cores = [CORES_GRAFICO[2], CORES_GRAFICO[3]]
        
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=valores,
                marker=dict(colors=cores),
                textposition='inside',
                textinfo='label+percent'
            )
        ])
        
        fig.update_layout(
            title="Taxa de Aceitação",
            height=400
        )
        
        return fig
    
    @staticmethod
    def grafico_barras_por_especialidade(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Gera gráfico de barras horizontais com especialidades mais solicitadas.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            top_n (int): Número de especialidades a exibir
            
        Returns:
            go.Figure: Gráfico Plotly
        """
        if df.empty:
            return _criar_grafico_vazio("Sem dados para exibir")
        
        # Filtrar valores em branco
        df_filtrado = df[df['especialidade'].notna() & (df['especialidade'] != '') & (df['especialidade'].astype(str).str.strip() != '')]
        
        if df_filtrado.empty:
            return _criar_grafico_vazio("Nenhuma especialidade registrada")
        
        especialidades = df_filtrado['especialidade'].value_counts().head(top_n).sort_values(ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(
                y=especialidades.index,
                x=especialidades.values,
                orientation='h',
                marker=dict(color='#0078d4'),
                text=especialidades.values,
                textposition='auto'
            )
        ])
        
        max_valor = especialidades.values.max()
        fig.update_layout(
            title=f"Top {top_n} Especialidades Mais Solicitadas",
            xaxis_title="Quantidade",
            yaxis_title="Especialidade",
            xaxis=dict(range=[0, max_valor * 1.5]),
            height=400,
            template='plotly_white',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def grafico_barras_por_hospital(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Gera gráfico de barras com hospitais mais solicitados.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            top_n (int): Número de hospitais a exibir
            
        Returns:
            go.Figure: Gráfico Plotly
        """
        if df.empty:
            return _criar_grafico_vazio("Sem dados para exibir")
        
        # Filtrar valores em branco
        df_filtrado = df[df['hospital'].notna() & (df['hospital'] != '') & (df['hospital'].astype(str).str.strip() != '')]
        
        if df_filtrado.empty:
            return _criar_grafico_vazio("Nenhum hospital registrado")
        
        hospitais = df_filtrado['hospital'].value_counts().head(top_n).sort_values(ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(
                x=hospitais.values,
                y=hospitais.index,
                orientation='h',
                marker=dict(color='#107c10'),
                text=hospitais.values,
                textposition='auto'
            )
        ])
        
        max_valor = hospitais.values.max()
        fig.update_layout(
            title=f"Top {top_n} Hospitais com Mais Solicitações",
            xaxis_title="Quantidade",
            yaxis_title="Hospital",
            xaxis=dict(range=[0, max_valor * 1.5]),
            height=400,
            template='plotly_white',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def grafico_barras_por_cidade(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Gera gráfico de barras com cidades com mais solicitações.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            top_n (int): Número de cidades a exibir
            
        Returns:
            go.Figure: Gráfico Plotly
        """
        if df.empty:
            return _criar_grafico_vazio("Sem dados para exibir")
        
        # Filtrar valores em branco
        df_filtrado = df[df['cidade'].notna() & (df['cidade'] != '') & (df['cidade'].astype(str).str.strip() != '')]
        
        if df_filtrado.empty:
            return _criar_grafico_vazio("Nenhuma cidade registrada")
        
        cidades = df_filtrado['cidade'].value_counts().head(top_n).sort_values(ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(
                x=cidades.values,
                y=cidades.index,
                orientation='h',
                marker=dict(color='#50a896'),
                text=cidades.values,
                textposition='auto'
            )
        ])
        
        max_valor = cidades.values.max()
        fig.update_layout(
            title=f"Top {top_n} Cidades com Mais Solicitações",
            xaxis_title="Quantidade",
            yaxis_title="Cidade",
            xaxis=dict(range=[0, max_valor * 1.5]),
            height=400,
            template='plotly_white',
            xaxis_tickangle=0,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def grafico_linha_tendencia_temporal(df: pd.DataFrame) -> go.Figure:
        """
        Gera gráfico de linha mostrando tendência temporal.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            
        Returns:
            go.Figure: Gráfico Plotly
        """
        if df.empty:
            return _criar_grafico_vazio("Sem dados para exibir")
        
        df_temp = df.copy()
        df_temp['data'] = pd.to_datetime(df_temp['data'], errors='coerce')
        df_temp = df_temp.sort_values('data')
        
        # Agrupar por mês
        df_temp['periodo'] = df_temp['data'].dt.to_period('M')
        
        # Calcular aceitação por mês
        tendencia = df_temp.groupby('periodo').agg({
            'aceito': ['sum', 'count']
        }).reset_index()
        
        tendencia.columns = ['periodo', 'aceitas', 'total']
        tendencia['taxa'] = (tendencia['aceitas'] / tendencia['total'] * 100).round(2)
        
        # Formatar meses abreviados
        meses_abrev = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                      'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        labels_x = []
        for periodo_val in tendencia['periodo']:
            month = periodo_val.month
            labels_x.append(meses_abrev[month - 1])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=labels_x,
            y=tendencia['taxa'],
            mode='lines+markers',
            name='Taxa de Aceitação (%)',
            line=dict(color=CORES_GRAFICO[0], width=3),
            marker=dict(size=8)
        ))
        
        max_taxa = tendencia['taxa'].max()
        fig.update_layout(
            title="Tendência de Taxa de Aceitação",
            xaxis_title="Mês",
            yaxis_title="Taxa (%)",
            yaxis=dict(range=[0, max_taxa * 1.5]),
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    @staticmethod
    def grafico_heatmap_hora_do_dia(df: pd.DataFrame) -> go.Figure:
        """
        Gera heatmap mostrando distribuição de solicitações por hora do dia.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            
        Returns:
            go.Figure: Gráfico Plotly
        """
        if df.empty:
            return _criar_grafico_vazio("Sem dados para exibir")
        
        df_temp = df.copy()
        df_temp['data'] = pd.to_datetime(df_temp['data'], errors='coerce')
        df_temp['hora'] = df_temp['data'].dt.hour
        df_temp['dia_semana'] = df_temp['data'].dt.day_name()
        
        # Criar matriz de contagem
        heatmap_data = df_temp.groupby(['dia_semana', 'hora']).size().unstack(fill_value=0)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='YlOrRd'
        ))
        
        fig.update_layout(
            title="Distribuição de Solicitações por Hora do Dia",
            xaxis_title="Hora do Dia",
            yaxis_title="Dia da Semana",
            height=400
        )
        
        return fig

    @staticmethod
    def grafico_barras_por_leito(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Gera gráfico de barras com leitos mais solicitados.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            top_n (int): Número de top leitos a exibir
            
        Returns:
            go.Figure: Gráfico Plotly
        """
        if df.empty:
            return _criar_grafico_vazio("Sem dados para exibir")
        
        # Filtrar valores em branco
        df_filtrado = df[df['leito_solicitado'].notna() & (df['leito_solicitado'] != '') & (df['leito_solicitado'].astype(str).str.strip() != '')]
        
        if df_filtrado.empty:
            return _criar_grafico_vazio("Nenhum leito registrado")
        
        leitos = df_filtrado['leito_solicitado'].value_counts().head(top_n).sort_values(ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(
                x=leitos.values,
                y=leitos.index,
                orientation='h',
                marker=dict(color='#005a9e'),
                text=leitos.values,
                textposition='auto'
            )
        ])
        
        max_valor = leitos.values.max()
        fig.update_layout(
            title="Top Leitos Solicitados",
            xaxis_title="Quantidade",
            yaxis_title="Leito",
            xaxis=dict(range=[0, max_valor * 1.5]),
            hovermode='y unified',
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        return fig

    @staticmethod
    def grafico_barras_por_medico(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Gera gráfico de barras com médicos mais solicitados.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            top_n (int): Número de top médicos a exibir
            
        Returns:
            go.Figure: Gráfico Plotly
        """
        if df.empty:
            return _criar_grafico_vazio("Sem dados para exibir")
        
        # Filtrar valores em branco
        df_filtrado = df[df['nome_medico'].notna() & (df['nome_medico'] != '') & (df['nome_medico'].astype(str).str.strip() != '')]
        
        if df_filtrado.empty:
            return _criar_grafico_vazio("Nenhum médico registrado")
        
        medicos = df_filtrado['nome_medico'].value_counts().head(top_n).sort_values(ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(
                x=medicos.values,
                y=medicos.index,
                orientation='h',
                marker=dict(color='#107c10'),
                text=medicos.values,
                textposition='auto'
            )
        ])
        
        max_valor = medicos.values.max()
        fig.update_layout(
            title="Top Médicos Solicitantes",
            xaxis_title="Quantidade",
            yaxis_title="Médico",
            xaxis=dict(range=[0, max_valor * 1.5]),
            hovermode='y unified',
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        return fig

    @staticmethod
    def grafico_barras_por_justificativa(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Gera gráfico de barras com justificativas mais utilizadas.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            top_n (int): Número de top justificativas a exibir
            
        Returns:
            go.Figure: Gráfico Plotly
        """
        if df.empty:
            return _criar_grafico_vazio("Sem dados para exibir")
        
        # Converter para string e limpar espaços
        df_temp = df.copy()
        df_temp['codigo_justificativa'] = df_temp['codigo_justificativa'].astype(str).str.strip()
        
        # Filtrar valores vazios e inválidos
        df_filtrado = df_temp[
            (df_temp['codigo_justificativa'].notna()) & 
            (df_temp['codigo_justificativa'] != '') & 
            (df_temp['codigo_justificativa'] != 'nan') &
            (df_temp['codigo_justificativa'].str.len() > 0)
        ]
        
        if df_filtrado.empty:
            return _criar_grafico_vazio("Nenhuma justificativa registrada")
        
        justificativas = df_filtrado['codigo_justificativa'].value_counts().head(top_n)
        
        # Filtrar apenas justificativas com contagem > 0
        justificativas = justificativas[justificativas > 0].sort_values(ascending=True)
        
        if justificativas.empty:
            return _criar_grafico_vazio("Nenhuma justificativa com registros")
        
        fig = go.Figure(data=[
            go.Bar(
                x=justificativas.values,
                y=justificativas.index,
                orientation='h',
                marker=dict(color='#d13438'),
                text=justificativas.values,
                textposition='auto'
            )
        ])
        
        max_valor = justificativas.values.max()
        fig.update_layout(
            title="Justificativas Mais Utilizadas",
            xaxis_title="Quantidade",
            yaxis_title="Justificativa",
            xaxis=dict(range=[0, max_valor * 1.5]),
            hovermode='y unified',
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        return fig


def _criar_grafico_vazio(mensagem: str) -> go.Figure:
    """
    Cria um gráfico vazio com mensagem.
    
    Args:
        mensagem (str): Mensagem a exibir
        
    Returns:
        go.Figure: Gráfico vazio com anotação
    """
    fig = go.Figure()
    fig.add_annotation(
        text=mensagem,
        showarrow=False,
        font=dict(size=14, color='gray')
    )
    fig.update_layout(
        height=400,
        template='plotly_white',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig
