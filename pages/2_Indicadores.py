"""
Página de Indicadores - Dashboard com análises e gráficos.
Exibe KPIs e visualizações para tomada de decisão.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.database import GerenciadorDados
from modules.charts import GeradorGraficos
from modules.filters import FiltrosAvancados
from utils.constants import CIDADES, ESPECIALIDADES, HOSPITAIS, LINHAS_TABELA_INDICADORES
from utils.helpers import formatar_percentual, calcular_taxa_percentual


def exibir_cards_kpi(stats: dict):
    """
    Exibe cards com KPIs principais.
    
    Args:
        stats (dict): Dicionário com estatísticas
    """
    st.header("📈 Indicadores Principais")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total de Solicitações",
            value=stats['total_solicitacoes'],
            delta=None,
            help="Número total de solicitações registradas"
        )
    
    with col2:
        st.metric(
            label="Solicitações Aceitas",
            value=stats['total_aceitas'],
            delta=None,
            help="Número de solicitações que foram aceitas"
        )
    
    with col3:
        st.metric(
            label="Solicitações Recusadas",
            value=stats['total_recusadas'],
            delta=None,
            help="Número de solicitações que foram recusadas"
        )

    with col4:
        st.metric(
            label="Taxa de Aceitação",
            value=f"{stats['taxa_aceitacao']:.1f}%",
            delta=None,
            help="Percentual de solicitações aceitas"
        )
    
    with col5:
        st.metric(
            label="Cidade Principal",
            value=stats['cidade_mais_solicitada'],
            delta=None,
            help="Cidade com mais solicitações"
        )
    
    st.divider()


def exibir_filtros_data():
    """
    Exibe filtros de data para análises.
    
    Returns:
        tuple: (data_inicio, data_fim)
    """
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Inicializar session state se não existir
    if 'filtro_data' not in st.session_state:
        st.session_state.filtro_data = 'mes'
    
    with col1:
        if st.button("Hoje", use_container_width=True, key="btn_hoje"):
            st.session_state.filtro_data = 'hoje'
            st.rerun()
    
    with col2:
        if st.button("Semana", use_container_width=True, key="btn_semana"):
            st.session_state.filtro_data = 'semana'
            st.rerun()
    
    with col3:
        if st.button("Mês", use_container_width=True, key="btn_mes"):
            st.session_state.filtro_data = 'mes'
            st.rerun()
    
    with col4:
        if st.button("Ano", use_container_width=True, key="btn_ano"):
            st.session_state.filtro_data = 'ano'
            st.rerun()
    
    with col5:
        if st.button("Personalizado", use_container_width=True, key="btn_personalizado"):
            st.session_state.filtro_data = 'personalizado'
            st.rerun()
    
    filtro = st.session_state.filtro_data
    hoje = datetime.now()
    
    if filtro == 'hoje':
        data_inicio = hoje.replace(hour=0, minute=0, second=0, microsecond=0)
        data_fim = hoje
    elif filtro == 'semana':
        data_inicio = hoje - timedelta(days=hoje.weekday())
        data_fim = hoje
    elif filtro == 'mes':
        data_inicio = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        data_fim = hoje
    elif filtro == 'ano':
        data_inicio = hoje.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        data_fim = hoje
    else:  # personalizado
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            data_inicio = st.date_input(
                "Data Início",
                value=datetime.now() - timedelta(days=30),
                format="DD/MM/YYYY"
            )
        with col_p2:
            data_fim = st.date_input(
                "Data Fim",
                value=datetime.now(),
                format="DD/MM/YYYY"
            )
        
        if data_inicio is not None:
            data_inicio = datetime.combine(data_inicio, datetime.min.time())
        else:
            data_inicio = datetime.now() - timedelta(days=30)
        
        if data_fim is not None:
            data_fim = datetime.combine(data_fim, datetime.max.time())
        else:
            data_fim = datetime.now()
    
    return data_inicio, data_fim


def exibir_graficos(df: pd.DataFrame):
    """
    Exibe gráficos principais do dashboard.
    
    Args:
        df (pd.DataFrame): DataFrame filtrado com dados
    """
    st.header("📊 Análises Visuais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_barras = GeradorGraficos.grafico_barras_solicitacoes_por_periodo(df, periodo='mes')
        st.plotly_chart(fig_barras, use_container_width=True)
    
    with col2:
        fig_pizza = GeradorGraficos.grafico_pizza_taxa_aceitacao(df)
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    # Segunda linha
    col3, col4 = st.columns(2)
    
    with col3:
        fig_cidades = GeradorGraficos.grafico_barras_por_cidade(df)
        st.plotly_chart(fig_cidades, use_container_width=True)
    
    with col4:
        fig_tendencia = GeradorGraficos.grafico_linha_tendencia_temporal(df)
        st.plotly_chart(fig_tendencia, use_container_width=True)
    
    # Terceira linha
    col5, col6 = st.columns(2)
    
    with col5:
        fig_leitos = GeradorGraficos.grafico_barras_por_leito(df)
        st.plotly_chart(fig_leitos, use_container_width=True)
    
    with col6:
        fig_medicos = GeradorGraficos.grafico_barras_por_medico(df)
        st.plotly_chart(fig_medicos, use_container_width=True)
    
    # Quarta linha
    col7, col8 = st.columns(2)
    
    with col7:
        fig_justificativas = GeradorGraficos.grafico_barras_por_justificativa(df)
        st.plotly_chart(fig_justificativas, use_container_width=True)


def exibir_tabelas_analise(df: pd.DataFrame):
    """
    Exibe tabelas de análise detalhada.
    
    Args:
        df (pd.DataFrame): DataFrame com dados
    """
    st.header("📋 Tabelas de Análise")
    
    tab1, tab2, tab3 = st.tabs(
        ["Leitos", "Médicos", "Cidades"]
    )
    
    with tab1:
        leitos = df[df['leito_solicitado'].notna() & (df['leito_solicitado'].astype(str).str.strip() != '')]['leito_solicitado'].value_counts().head(LINHAS_TABELA_INDICADORES)
        df_leitos = pd.DataFrame({
            'Leito': leitos.index,
            'Quantidade': leitos.values,
            'Percentual': [f"{(v/len(df)*100):.1f}%" for v in leitos.values]
        })
        st.dataframe(df_leitos, use_container_width=True, hide_index=True)
    
    with tab2:
        medicos = df[df['nome_medico'].notna() & (df['nome_medico'].astype(str).str.strip() != '')]['nome_medico'].value_counts().head(LINHAS_TABELA_INDICADORES)
        df_med = pd.DataFrame({
            'Médico': medicos.index,
            'Quantidade': medicos.values,
            'Percentual': [f"{(v/len(df)*100):.1f}%" for v in medicos.values]
        })
        st.dataframe(df_med, use_container_width=True, hide_index=True)
    
    with tab3:
        cidades = df[df['cidade'].notna() & (df['cidade'].astype(str).str.strip() != '')]['cidade'].value_counts().head(LINHAS_TABELA_INDICADORES)
        df_cid = pd.DataFrame({
            'Cidade': cidades.index,
            'Quantidade': cidades.values,
            'Percentual': [f"{(v/len(df)*100):.1f}%" for v in cidades.values]
        })
        st.dataframe(df_cid, use_container_width=True, hide_index=True)


def exibir_relatorio_customizado(df: pd.DataFrame):
    """
    Permite criar relatório customizado e exportar.
    
    Args:
        df (pd.DataFrame): DataFrame com dados
    """
    st.header("📄 Relatório Customizado")
    
    with st.expander("Criar relatório customizado"):
        colunas_disponiveis = [
            'data', 'nome_paciente', 'cidade', 'hospital',
            'solicitante', 'diagnostico', 'leito_solicitado',
            'especialidade', 'aceito', 'nome_medico',
            'nome_recepcionista', 'codigo_justificativa'
        ]
        
        colunas_selecionadas = st.multiselect(
            "Selecione as colunas para incluir no relatório",
            options=colunas_disponiveis,
            default=colunas_disponiveis[:5],
            help="Escolha quais informações deseja no relatório"
        )
        
        if colunas_selecionadas:
            df_relatorio = df[colunas_selecionadas].copy()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Download CSV
                csv = df_relatorio.to_csv(index=False, encoding='utf-8').encode('utf-8')
                st.download_button(
                    label="📥 Baixar como CSV",
                    data=csv,
                    file_name=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Previsão: implementar exportação para Excel/PDF
                st.info("💡 Exportação para Excel em desenvolvimento")


def main():
    """
    Função principal da página de Indicadores.
    """
    gerenciador = GerenciadorDados()
    
    # Exibir KPIs
    stats = gerenciador.obter_estatisticas()
    exibir_cards_kpi(stats)
    
    # Filtros de data
    st.header("📅 Período de Análise")
    data_inicio, data_fim = exibir_filtros_data()
    st.divider()
    
    # Obter e filtrar dados
    df = gerenciador.obter_todas_solicitacoes()
    
    if not df.empty:
        # Filtrar por data
        df_filtrado = FiltrosAvancados.filtrar_por_data(df, data_inicio, data_fim)
        
        if df_filtrado.empty:
            st.info("Nenhum dado disponível para o período selecionado.")
        else:
            # Exibir gráficos
            exibir_graficos(df_filtrado)
            
            st.divider()
            
            # Exibir tabelas
            exibir_tabelas_analise(df_filtrado)
            
            st.divider()
            
            # Exibir relatório customizado
            exibir_relatorio_customizado(df_filtrado)
    else:
        st.info("Nenhum dado registrado. Acesse a página inicial para adicionar solicitações!")


if __name__ == "__main__":
    main()
