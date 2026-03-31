"""
Aplicação - Sistema de Gerenciamento de Solicitações Hospitalares do SUS Fácil.
Desenvolvido em Streamlit para facilitar o preenchimento, visualização e análise
de dados de internações hospitalares.
"""

import streamlit as st
from datetime import datetime
import sys
import os
import time

# Adicionar diretório ao path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.constants import (
    APP_TITLE, APP_ICON, THEME_COLOR, SIDEBAR_ICON
)
from modules.database import GerenciadorDados


# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Sistema de Gerenciamento de Solicitações Hospitalares do SUS Fácil v1.0"
    }
)

st.title(APP_TITLE)
st.caption("Sistema de Gerenciamento de Solicitações Hospitalares do SUS Fácil")

# Configurar locale para português
import locale
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR')
    except:
        pass  # Fallback para locale padrão do sistema


# ============================================================================
# CSS CUSTOMIZADO
# ============================================================================
st.markdown("""
    <style>
        /* Estilo geral */
        :root {
            --primary-color: #1f77b4;
            --success-color: #2ca02c;
            --danger-color: #d62728;
            --warning-color: #ff7f0e;
        }
        
        /* Barra lateral */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #F2F2F2 0%, #F2F2F2 100%);
        }
        
        /* Cards de métricas */
        [data-testid="metric-container"] {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Botões */
        .stButton>button {
            border-radius: 6px;
            font-weight: 600;
            padding: 10px 20px;
            transition: all 0.3s ease;
        }
        
        .stButton>button[kind="primary"] {
            background: linear-gradient(90deg, #1f77b4 0%, #2d5a8c 100%);
            color: white;
            border: none;
        }
        
        .stButton>button[kind="secondary"] {
            background-color: #e8eef2;
            color: #1f77b4;
            border: 2px solid #1f77b4;
        }
        
        /* Entrada de dados */
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select {
            border-radius: 6px;
            border: 1px solid #ccc;
            padding: 8px 12px;
        }
        
        .stTextInput>div>div>input:focus,
        .stNumberInput>div>div>input:focus {
            border-color: #1f77b4;
            box-shadow: 0 0 5px rgba(31, 119, 180, 0.3);
        }
        
        /* Abas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            border-radius: 6px 6px 0px 0px;
            padding: 0px 20px;
            background-color: #f0f2f6;
            border-bottom: 3px solid transparent;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #1f77b4;
            color: white;
            border-bottom: 3px solid #1f77b4;
        }
        
        /* Mensagens */
        .stAlert {
            border-radius: 6px;
            padding: 15px;
        }
        
        /* Tabelas */
        .stDataFrame {
            border-radius: 6px;
            overflow: hidden;
        }
        
        /* Divisor */
        .stDivider {
            margin: 20px 0;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #f0f2f6;
            border-radius: 6px;
            padding: 10px;
        }
        
        /* Títulos */
        h1, h2, h3 {
            color: #1f77b4;
        }
        
        /* Rodapé */
        footer {
            text-align: center;
            padding: 20px;
            font-size: 12px;
            color: #666;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# BARRA LATERAL (INFO, UPLOAD, FOOTER)
# ============================================================================
with st.sidebar:
    gerenciador = GerenciadorDados()
    
    # ===== SEÇÃO 1: ESTATÍSTICAS =====
    st.subheader("📊 Estatísticas Rápidas")
    stats = gerenciador.obter_estatisticas()
    
    # Exibir métricas em formato de cards, uma embaixo da outra
    st.metric(
        "Solicitações",
        stats['total_solicitacoes'],
        help="Total de solicitações registradas"
    )
    
    st.metric(
        "Taxa de Aceitação",
        f"{stats['taxa_aceitacao']:.2f}%",
        help="Percentual de solicitações aceitas"
    )
    
    st.metric(
        "Solicitações Aceitas",
        stats['total_aceitas'],
        help="Total de solicitações aceitas"
    )
    
    st.metric(
        "Solicitações Recusadas",
        stats['total_recusadas'],
        help="Total de solicitações recusadas"
    )
    
    st.markdown(f"**Cidade principal:** {stats['cidade_mais_solicitada']}")
    
    st.divider()
    
    # ===== SEÇÃO 2: IMPORTAR DADOS =====
    st.subheader("📤 Importar Dados")
    
    uploaded_file = st.file_uploader(
        "Selecione um arquivo CSV",
        type=["csv"],
        help="Carregue um CSV com as colunas: data, nome_paciente, cidade, hospital, diagnostico, leito_solicitado, especialidade, aceito, nome_medico, nome_recepcionista, codigo_justificativa"
    )
    
    if uploaded_file is not None:
        try:
            # Ler o CSV
            df_importado = pd.read_csv(uploaded_file)
            
            # Validar colunas obrigatórias
            colunas_obrigatorias = [
                'data', 'nome_paciente', 'cidade', 'hospital', 
                'diagnostico', 'leito_solicitado', 'especialidade', 
                'aceito', 'nome_medico', 'nome_recepcionista', 'codigo_justificativa'
            ]
            
            colunas_faltantes = [col for col in colunas_obrigatorias if col not in df_importado.columns]
            
            if colunas_faltantes:
                st.error(f"❌ Colunas faltantes: {', '.join(colunas_faltantes)}")
            else:
                # Importar dados
                total_importado = 0
                for idx, row in df_importado.iterrows():
                    dados = {
                        'data': row.get('data', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                        'nome_paciente': str(row.get('nome_paciente', '')),
                        'cidade': str(row.get('cidade', '')),
                        'hospital': str(row.get('hospital', '')),
                        'solicitante': str(row.get('hospital', '')),
                        'diagnostico': str(row.get('diagnostico', '')),
                        'leito_solicitado': str(row.get('leito_solicitado', '')),
                        'especialidade': str(row.get('especialidade', '')),
                        'aceito': bool(row.get('aceito', False)),
                        'nome_medico': str(row.get('nome_medico', '')),
                        'nome_recepcionista': str(row.get('nome_recepcionista', '')),
                        'codigo_justificativa': str(row.get('codigo_justificativa', ''))
                    }
                    
                    if gerenciador.inserir_solicitacao(dados):
                        total_importado += 1
                
                st.success(f"✅ {total_importado} solicitação(ões) importada(s) com sucesso!")
                st.rerun()
        
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {str(e)}")
    
    st.divider()
    
    # ===== SEÇÃO 3: INFORMAÇÕES =====
    st.subheader("ℹ️ Sobre o Sistema")
    
    with st.expander("📋 Instruções de Uso", expanded=False):
        st.markdown("""
        **Como usar a Plataforma:**
        
        1. **Registrar Solicitação**
           - Acesse a página inicial da plataforma
           - Preencha todos os campos do formulário
           - Clique em "Salvar Solicitação" para registrar os dados
        
        2. **Consultar Dados**
           - Use os filtros disponíveis para refinar sua busca
           - Visualize todas as solicitações registradas na tabela
        
        3. **Gerenciar Solicitações**
           - Edite informações de solicitações já cadastradas
           - Exclua registros desnecessários
        
        4. **Análise de Dados**
           - Acesse a página "Indicadores" para visualizar gráficos e métricas
           - Exporte dados em formato CSV para análises externas
        """)
    
    st.divider()
    
    # ===== RODAPÉ =====
    st.markdown("""
    <footer style='text-align: center; padding: 15px 0; font-size: 11px; color: #999;'>
        <strong>SUS Fácil Solicitações v1.0</strong><br>
        Sistema de Gerenciamento de Solicitações Hospitalares do SUS Fácil<br>
        Dezembro 2025<br>
        <a href='mailto:erix.freitas@santacasaitajuba.com.br'>📧 Suporte</a>
    </footer>
    """, unsafe_allow_html=True)


# ============================================================================
# IMPORTAÇÕES ADICIONAIS
# ============================================================================
import pandas as pd
from modules.filters import FiltrosAvancados
from utils.constants import (
    CIDADES, ESPECIALIDADES, LEITOS, MEDICOS, RECEPCIONISTAS,
    CODIGOS_JUSTIFICATIVA, LINHAS_POR_PAGINA
)
from utils.helpers import (
    formatar_data_br, validar_nome,
    exibir_mensagem_sucesso, exibir_mensagem_erro, formatar_data_sql
)


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================
def exibir_formulario_edicao(gerenciador, id_solicitacao):
    """
    Exibe o formulário para edição de uma solicitação existente.
    """
    # Obter dados da solicitação
    solicitacao = gerenciador.obter_solicitacao_por_id(id_solicitacao)
    
    if solicitacao is None:
        st.error(f"Solicitação com ID {id_solicitacao} não encontrada")
        return
    
    st.header(f"✏️ Editar Solicitação (ID: {id_solicitacao})")
    
    # Inicializar contador para forçar nova instância do formulário
    if 'form_edicao_counter' not in st.session_state:
        st.session_state.form_edicao_counter = 0
    
    form_key = f'form_edicao_solicitacao_{st.session_state.form_edicao_counter}'
    
    with st.form(key=form_key):
        # Primeira linha - Data e Nome do Paciente
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input(
                "Data da Solicitação *",
                value=pd.to_datetime(solicitacao.get('data')).date(),
                format="DD/MM/YYYY",
                help="Data em que a solicitação foi feita"
            )
        
        with col2:
            nome_paciente = st.text_input(
                "Nome do Paciente *",
                value=solicitacao.get('nome_paciente', ''),
                max_chars=100
            )
        
        # Segunda linha - Cidade e Hospital Solicitante
        col3, col4 = st.columns(2)
        with col3:
            cidade = st.selectbox(
                "Cidade *",
                options=[""] + CIDADES,
                index=CIDADES.index(solicitacao.get('cidade', '')) + 1 if solicitacao.get('cidade', '') in CIDADES else 0
            )
        
        with col4:
            hospital_solicitante = st.text_input(
                "Hospital Solicitante *",
                value=solicitacao.get('hospital', ''),
                max_chars=200
            )
        
        # Terceira linha - Diagnóstico e Especialidade
        col5, col6 = st.columns(2)
        with col5:
            diagnostico = st.text_input(
                "Diagnóstico *",
                value=solicitacao.get('diagnostico', ''),
                max_chars=200
            )
        
        with col6:
            especialidade = st.text_input(
                "Especialidade *",
                value=solicitacao.get('especialidade', ''),
                max_chars=100
            )
        
        # Quarta linha - Leito Solicitado + Nome do Médico
        col7, col8 = st.columns(2)
        with col7:
            leito_idx = LEITOS.index(solicitacao.get('leito_solicitado', '')) + 1 if solicitacao.get('leito_solicitado', '') in LEITOS else 0
            leito_solicitado = st.selectbox(
                "Leito Solicitado *",
                options=[""] + LEITOS,
                index=leito_idx
            )

        with col8:
            medico_idx = MEDICOS.index(solicitacao.get('nome_medico', '')) if solicitacao.get('nome_medico', '') in MEDICOS else 0
            nome_medico = st.selectbox(
                "Nome do Médico *",
                options=[""] + MEDICOS,
                index=medico_idx + 1
            )
        
        # Quinta linha - Recepcionista + Solicitação Aceita
        col9, col10 = st.columns(2)
        with col9:
            recep_idx = RECEPCIONISTAS.index(solicitacao.get('nome_recepcionista', '')) if solicitacao.get('nome_recepcionista', '') in RECEPCIONISTAS else 0
            nome_recepcionista = st.selectbox(
                "Nome da Recepcionista *",
                options=[""] + RECEPCIONISTAS,
                index=recep_idx + 1
            )
        
        with col10:
            aceito_atual = "Sim" if solicitacao.get('aceito') else "Não"
            aceito_idx = ["", "Sim", "Não"].index(aceito_atual) if aceito_atual in ["Sim", "Não"] else 0
            aceito_display = st.selectbox(
                "Solicitação Aceita *",
                options=["", "Sim", "Não"],
                index=aceito_idx
            )
            aceito = True if aceito_display == "Sim" else False
        
        # Sexta linha - Código da Justificativa (condicional, apenas se não aceito)
        if aceito_display == "Não":
            col11 = st.columns(1)[0]
            with col11:
                opcoes_justificativa = {f"{k} - {v}": k for k, v in CODIGOS_JUSTIFICATIVA.items()}
                justificativa_atual = f"{solicitacao.get('codigo_justificativa')} - {CODIGOS_JUSTIFICATIVA.get(solicitacao.get('codigo_justificativa'), '')}"
                justificativa_idx = list(opcoes_justificativa.keys()).index(justificativa_atual) + 1 if justificativa_atual in opcoes_justificativa else 0
                codigo_justificativa_display = st.selectbox(
                    "Código da Justificativa * (Obrigatório para recusadas)",
                    options=[""] + list(opcoes_justificativa.keys()),
                    index=justificativa_idx
                )
                codigo_justificativa = opcoes_justificativa.get(codigo_justificativa_display, "")
        else:
            codigo_justificativa_display = ""
            codigo_justificativa = ""
        
        # Botões
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submitted = st.form_submit_button(
                "💾 Salvar Alterações",
                use_container_width=True,
                type="primary"
            )
        
        with col_btn2:
            cancelar = st.form_submit_button(
                "❌ Cancelar",
                use_container_width=True
            )
        
        if cancelar:
            st.session_state.modo_edicao = False
            st.rerun()
        
        if submitted:
            # Validações básicas
            if not nome_paciente or not nome_paciente.strip():
                st.error("Nome do paciente é obrigatório")
                return
            
            if not cidade or cidade == "":
                st.error("Cidade é obrigatória")
                return
            
            if not hospital_solicitante or not hospital_solicitante.strip():
                st.error("Hospital Solicitante é obrigatório")
                return
            
            if not diagnostico or not diagnostico.strip():
                st.error("Diagnóstico é obrigatório")
                return
            
            if not especialidade or not especialidade.strip():
                st.error("Especialidade é obrigatória")
                return
            
            if not nome_medico or nome_medico == "":
                st.error("Nome do Médico é obrigatório")
                return
            
            if not nome_recepcionista or nome_recepcionista == "":
                st.error("Nome da Recepcionista é obrigatório")
                return
            
            if not aceito_display or aceito_display == "":
                st.error("Informe se a solicitação foi aceita")
                return
            
            # Validar justificativa apenas se não aceito
            if aceito_display == "Não" and (not codigo_justificativa_display or codigo_justificativa_display == ""):
                st.error("Código da Justificativa é obrigatório para solicitações recusadas")
                return
            
            # Preparar dados para atualização
            dados_atualizados = {
                'data': formatar_data_sql(datetime.combine(data, datetime.min.time())),
                'nome_paciente': nome_paciente.strip(),
                'cidade': cidade,
                'hospital': hospital_solicitante.strip(),
                'solicitante': hospital_solicitante.strip(),
                'diagnostico': diagnostico.strip(),
                'leito_solicitado': leito_solicitado,
                'especialidade': especialidade.strip(),
                'aceito': aceito,
                'nome_medico': nome_medico,
                'nome_recepcionista': nome_recepcionista,
                'codigo_justificativa': codigo_justificativa
            }
            
            # Atualizar no banco de dados
            if gerenciador.atualizar_solicitacao(id_solicitacao, dados_atualizados):
                st.success("✓ Solicitação atualizada com sucesso!")
                time.sleep(1)
                st.session_state.form_edicao_counter += 1  # Incrementar contador para nova instância
                st.session_state.modo_edicao = False
                st.rerun()
            else:
                st.error("❌ Erro ao atualizar solicitação")


def exibir_formulario():
    """
    Exibe o formulário para preenchimento de nova solicitação.
    Todos os campos são obrigatórios.
    """
    st.header("📋 Novo Registro de Solicitação")
    
    # Exibir mensagem de sucesso se solicitação foi registrada
    if st.session_state.get('solicitacao_registrada', False):
        st.success("✅ Solicitação registrada com sucesso!")
        time.sleep(2)  # Mostrar mensagem por 2 segundos
        st.session_state.solicitacao_registrada = False
        st.rerun()
    
    # Inicializar contador para forçar nova instância do formulário
    if 'form_counter' not in st.session_state:
        st.session_state.form_counter = 0
    
    form_key = f'form_nova_solicitacao_{st.session_state.form_counter}'
    
    with st.form(key=form_key):
        # Primeira linha - Data e Nome do Paciente
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input(
                "Data da Solicitação *",
                value=datetime.now(),
                format="DD/MM/YYYY",
                help="Data em que a solicitação foi feita"
            )
        
        with col2:
            nome_paciente = st.text_input(
                "Nome do Paciente *",
                placeholder="Digite o nome completo",
                max_chars=100
            )
        
        # Segunda linha - Cidade e Hospital Solicitante
        col3, col4 = st.columns(2)
        with col3:
            cidade = st.selectbox(
                "Cidade *",
                help = "Selecione a cidade de origem",
                options=[""] + CIDADES
            )
        
        with col4:
            hospital_solicitante = st.text_input(
                "Hospital Solicitante *",
                placeholder="Digite o nome do hospital solicitante",
                max_chars=200
            )
        
        # Terceira linha - Diagnóstico e Especialidade
        col5, col6 = st.columns(2)
        with col5:
            diagnostico = st.text_input(
                "Diagnóstico *",
                placeholder="Digite o diagnóstico",
                max_chars=200
            )
        
        with col6:
            especialidade = st.text_input(
                "Especialidade *",
                placeholder="Digite a especialidade",
                max_chars=100
            )
        
        # Quarta linha - Leito Solicitado (agora com opções) + Nome do Médico (opções)
        col7, col8 = st.columns(2)
        with col7:
            leito_solicitado = st.selectbox(
                "Leito Solicitado *",
                options=[""] + LEITOS,
                help="Selecione o tipo de leito"
            )

        with col8:
            nome_medico = st.selectbox(
                "Nome do Médico *",
                options=[""] + MEDICOS,
                help="Selecione o médico responsável"
            )
        
        # Quinta linha - Nome da Recepcionista + Solicitação Aceita
        col9, col10 = st.columns(2)
        with col9:
            nome_recepcionista = st.selectbox(
                "Nome da Recepcionista *",
                options=[""] + RECEPCIONISTAS,
                help="Selecione a recepcionista responsável"
            )
        
        with col10:
            aceito_display = st.selectbox(
                "Solicitação Aceita *",
                options=["", "Sim", "Não"],
                help="Marque se a solicitação foi aceita ou não"
            )
            aceito = True if aceito_display == "Sim" else False
        
        # Sexta linha - Código da Justificativa (condicional, apenas se não aceito)
        if aceito_display == "Não":
            col11 = st.columns(1)[0]
            with col11:
                opcoes_justificativa = {f"{k} - {v}": k for k, v in CODIGOS_JUSTIFICATIVA.items()}
                codigo_justificativa_display = st.selectbox(
                    "Código da Justificativa * (Obrigatório para recusadas)",
                    options=[""] + list(opcoes_justificativa.keys()),
                    help="Selecione o código de justificativa"
                )
                codigo_justificativa = opcoes_justificativa.get(codigo_justificativa_display, "")
        else:
            codigo_justificativa_display = ""
            codigo_justificativa = ""
        
        # Botão de Envio
        submitted = st.form_submit_button(
            "✓ Registrar Solicitação",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            # Validar campos obrigatórios
            if not nome_paciente or not nome_paciente.strip():
                exibir_mensagem_erro("Nome do paciente é obrigatório")
                return
            
            if not validar_nome(nome_paciente):
                exibir_mensagem_erro("Nome do paciente inválido (mínimo 3 caracteres)")
                return
            
            if not cidade or cidade == "":
                exibir_mensagem_erro("Cidade é obrigatória")
                return
            
            if not hospital_solicitante or not hospital_solicitante.strip():
                exibir_mensagem_erro("Hospital Solicitante é obrigatório")
                return
            
            if not diagnostico or not diagnostico.strip():
                exibir_mensagem_erro("Diagnóstico é obrigatório")
                return
            
            if not especialidade or not especialidade.strip():
                exibir_mensagem_erro("Especialidade é obrigatória")
                return
            
            if not nome_medico or nome_medico == "":
                exibir_mensagem_erro("Nome do Médico é obrigatório")
                return
            
            if not nome_recepcionista or nome_recepcionista == "":
                exibir_mensagem_erro("Nome da Recepcionista é obrigatório")
                return
            
            if not aceito_display or aceito_display == "":
                exibir_mensagem_erro("Informe se a solicitação foi aceita")
                return
            
            # Validar justificativa apenas se não aceito
            if aceito_display == "Não" and (not codigo_justificativa_display or codigo_justificativa_display == ""):
                exibir_mensagem_erro("Código da Justificativa é obrigatório para solicitações recusadas")
                return
            
            # Preparar dados para inserção
            dados = {
                'data': formatar_data_sql(datetime.combine(data, datetime.min.time())),
                'nome_paciente': nome_paciente.strip(),
                'cidade': cidade,
                'hospital': hospital_solicitante.strip(),
                'solicitante': hospital_solicitante.strip(),
                'diagnostico': diagnostico.strip(),
                'leito_solicitado': leito_solicitado,
                'especialidade': especialidade.strip(),
                'aceito': aceito,
                'nome_medico': nome_medico,
                'nome_recepcionista': nome_recepcionista,
                'codigo_justificativa': codigo_justificativa
            }
            
            # Inserir no banco de dados
            gerenciador = GerenciadorDados()
            if gerenciador.inserir_solicitacao(dados):
                st.session_state.solicitacao_registrada = True
                st.session_state.form_counter += 1  # Incrementar contador para nova instância
                st.rerun()


def exibir_filtros():
    """
    Exibe a barra de filtros para a tabela de solicitações.
    
    Returns:
        dict: Dicionário com filtros aplicados
    """
    st.header("🔍 Filtros de Busca")
    
    with st.expander("Expandir/Fechar Filtros", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            data_inicio = st.date_input(
                "Data Início",
                value=None,
                help="Selecione a data de início do período"
            )
        
        with col2:
            data_fim = st.date_input(
                "Data Fim",
                value=None,
                help="Selecione a data de final do período"
            )
        
        with col3:
            busca_livre = st.text_input(
                "Busca Livre",
                placeholder="Paciente, hospital, médico...",
                help="Busque em múltiplos campos"
            )
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            cidade = st.selectbox(
                "Cidade",
                options=[None] + CIDADES,
                index=0,
                help="Filtrar por cidade"
            )
        
        with col5:
            especialidade = st.selectbox(
                "Especialidade",
                options=[None] + ESPECIALIDADES,
                index=0,
                help="Filtrar por especialidade"
            )
        
        with col6:
            status = st.selectbox(
                "Status",
                options=[None, True, False],
                format_func=lambda x: "Todos" if x is None else ("Aceitas" if x else "Recusadas"),
                help="Filtrar por status de aceitação"
            )
        
        # Botão de filtrar
        if st.button("🔎 Aplicar Filtros", use_container_width=True):
            pass  # Filtros serão aplicados no retorno
    
    return {
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'nome_paciente': busca_livre,
        'hospital': None,
        'especialidade': especialidade,
        'status': status,
        'cidade': cidade,
        'diagnostico': None,
        'busca_livre': busca_livre
    }


def exibir_tabela_solicitacoes():
    """
    Exibe a tabela com histórico de solicitações com opções de ação.
    """
    st.header("📊 Histórico de Solicitações")
    
    gerenciador = GerenciadorDados()
    
    # Obter filtros
    filtros = exibir_filtros()
    
    # Obter e filtrar dados
    df = gerenciador.obter_todas_solicitacoes()
    
    if not df.empty:
        # Aplicar filtros
        df_filtrado = FiltrosAvancados.aplicar_filtros_multiplos(df, filtros)
        
        if df_filtrado.empty:
            st.info("Nenhuma solicitação encontrada com os filtros aplicados.")
            return
        
        # Preparar dados para exibição
        df_exibicao = df_filtrado.copy()
        
        # Converter data se ainda não estiver em datetime
        if df_exibicao['data'].dtype != 'datetime64[ns]':
            df_exibicao['data'] = pd.to_datetime(df_exibicao['data'], errors='coerce')
        
        df_exibicao['data'] = df_exibicao['data'].dt.strftime("%d/%m/%Y %H:%M")
        df_exibicao['aceito'] = df_exibicao['aceito'].map(lambda x: "✓ Sim" if x else "✗ Não")
        
        # Formatar código de justificativa se disponível
        if 'codigo_justificativa' in df_exibicao.columns:
            df_exibicao['codigo_justificativa'] = df_exibicao['codigo_justificativa'].fillna('-')
        
        # Selecionar colunas para exibição
        colunas_exibicao = [
            'id', 'data', 'nome_paciente', 'cidade', 'hospital', 
            'diagnostico', 'especialidade', 'leito_solicitado',
            'aceito', 'nome_medico', 'nome_recepcionista', 'codigo_justificativa'
        ]
        df_exibicao = df_exibicao[colunas_exibicao]
        
        # Renomear colunas para exibição
        df_exibicao.columns = [
            'ID', 'Data', 'Paciente', 'Cidade', 'Hospital', 
            'Diagnóstico', 'Especialidade', 'Leito', 'Aceito', 
            'Médico', 'Recepcionista', 'Justificativa'
        ]
        
        # Exibir tabela com scroll
        st.dataframe(
            df_exibicao,
            use_container_width=True,
            height=400,
            hide_index=True
        )
        
        # Seção de Ações
        st.subheader("⚙️ Ações")
        
        # Linha 1: Seleção de ID
        col_id, col_spacer = st.columns([3, 2])
        with col_id:
            id_selecionado = st.number_input(
                "ID da Solicitação",
                min_value=0,
                value=0,
                help="Digite o ID da solicitação para realizar ações"
            )
        
        # Linha 2: Botões de ação com melhor organização
        st.markdown("<sub>**Ações Disponíveis:**</sub>", unsafe_allow_html=True)
        
        col_editar, col_deletar, col_exportar = st.columns(3)
        
        with col_editar:
            if st.button("✏️ Editar", use_container_width=True, key="btn_editar"):
                if id_selecionado > 0:
                    st.session_state.id_edicao = id_selecionado
                    st.session_state.modo_edicao = True
                    st.rerun()
                else:
                    st.error("⚠️ Selecione um ID válido", icon="⚠️")
        
        with col_deletar:
            if st.button("🗑️ Deletar", use_container_width=True, key="btn_deletar"):
                if id_selecionado > 0:
                    if gerenciador.deletar_solicitacao(id_selecionado):
                        st.success("✅ Solicitação deletada!", icon="✅")
                        st.rerun()
                else:
                    st.error("⚠️ Selecione um ID válido", icon="⚠️")
        
        with col_exportar:
            # Exportar para CSV
            csv = gerenciador.exportar_csv(filtrado=True, df_filtrado=df_filtrado)
            st.download_button(
                label="📥 Exportar",
                data=csv,
                file_name=f"solicitacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="btn_exportar"
            )
    else:
        st.info("Nenhuma solicitação registrada. Preencha o formulário acima para começar!")


# ============================================================================
# CONTEÚDO PRINCIPAL
# ============================================================================

# Verificar se está em modo de edição
if 'modo_edicao' not in st.session_state:
    st.session_state.modo_edicao = False

if 'id_edicao' not in st.session_state:
    st.session_state.id_edicao = None

if 'solicitacao_registrada' not in st.session_state:
    st.session_state.solicitacao_registrada = False

# Se está em modo de edição, mostrar formulário de edição
if st.session_state.modo_edicao and st.session_state.id_edicao:
    gerenciador = GerenciadorDados()
    exibir_formulario_edicao(gerenciador, st.session_state.id_edicao)
else:
    # Exibir formulário de novo registro
    exibir_formulario()

    st.divider()

    # Exibir tabela
    exibir_tabela_solicitacoes()
