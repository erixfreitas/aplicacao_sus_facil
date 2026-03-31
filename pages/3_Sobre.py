"""
Página Sobre - Informações sobre a Plataforma.
"""

import streamlit as st
from modules.database import GerenciadorDados


def main():
    """
    Função principal da página Sobre.
    """
    st.title("ℹ️ Sobre a Plataforma")
    
    st.markdown("""
    ## 🏥 Sistema de Gerenciamento de Solicitações Hospitalares do SUS Fácil
    
    **Versão:** 1.0  
    **Data de Lançamento:** Dezembro de 2025
    
    ### 📋 Descrição
    
    A plataforma é uma aplicação web desenvolvida em Streamlit que facilita o gerenciamento 
    e organização de solicitações de internação hospitalar do SUS Fácil. O sistema permite preenchimento 
    de formulários intuitivos, visualização de dados com filtros avançados e geração de 
    indicadores analíticos para tomada de decisão.
    
    ### ✨ Funcionalidades Principais
    
    - **📝 Formulário Intuitivo:** Preenchimento fácil com validação em tempo real
    - **📊 Dashboard Completo:** Gráficos e indicadores de desempenho
    - **🔍 Filtros Avançados:** Busca por múltiplos critérios
    - **📈 Análises Detalhadas:** Taxa de aceitação, distribuição por cidade, etc.
    - **💾 Persistência de Dados:** Armazenamento seguro em CSV
    - **📥 Exportação:** Relatórios customizados em CSV e PDF
    
    ### 🛠️ Tecnologias Utilizadas
    
    - **Streamlit:** Framework web para aplicações de dados
    - **Pandas:** Manipulação e análise de dados
    - **Plotly:** Gráficos interativos
    - **Python 3.8+:** Linguagem de programação
    
    ### 📊 Módulos da Aplicação
    
    | Módulo | Descrição |
    |--------|-----------|
    | `modules/database.py` | Operações CRUD com dados |
    | `modules/charts.py` | Geração de gráficos |
    | `modules/filters.py` | Filtros e buscas avançadas |
    | `utils/constants.py` | Configurações e constantes |
    | `utils/helpers.py` | Funções auxiliares |
    | `pages/1_home.py` | Página de preenchimento |
    | `pages/2_indicadores.py` | Dashboard de análises |
    | `pages/3_sobre.py` | Informações sobre o projeto |
    
    ### 🎯 Casos de Uso
    
    - Registrar solicitações de internação hospitalar do SUS Fácil
    - Acompanhar status de aceitação/recusa
    - Analisar tendências e padrões de internação
    - Gerar relatórios por período, cidade, hospital
    - Tomar decisões baseadas em dados
    
    ### 📞 Suporte
    
    Para dúvidas ou sugestões, entre em contato com a equipe de desenvolvimento.
    
    ### 📜 Licença
    
    Este projeto é destinado **exclusivamente para uso interno da empresa**. A **replicação, redistribuição,
                divulgação ou uso externo**, total ou parcial, **não é permitida** sem autorização formal.
    """)
    

if __name__ == "__main__":
    main()
