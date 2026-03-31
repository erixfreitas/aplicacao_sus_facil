# SUS Fácil - Sistema de Gerenciamento de Solicitações Hospitalares

Sistema web desenvolvido em **Streamlit** para gerenciar solicitações de internação hospitalar com formulários, visualização de dados, filtros avançados e indicadores analíticos.

## 🚀 Quick Start

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação
```bash
streamlit run app.py
```

A aplicação será aberta em: `http://localhost:8501`

## 📁 Estrutura do Projeto

```
projeto_sus_facil/
├── app.py                  # Arquivo principal - ponto de entrada
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
├── .gitignore             # Configuração Git
│
├── modules/               # Módulos de lógica
│   ├── database.py        # Gerenciamento de dados (CRUD)
│   ├── charts.py          # Geração de gráficos (Plotly)
│   ├── filters.py         # Lógica de filtros
│   └── __init__.py
│
├── pages/                 # Páginas da aplicação (navegação automática)
│   ├── 1_home.py          # Home - Preenchimento de dados
│   ├── 2_indicadores.py   # Indicadores - Dashboard com análises
│   ├── 3_sobre.py         # Sobre - Informações do projeto
│   └── __init__.py
│
├── utils/                 # Utilitários
│   ├── constants.py       # Constantes, dados estáticos e configurações
│   ├── helpers.py         # Funções auxiliares
│   ├── config.py          # Configuração de ambiente
│   └── __init__.py
│
├── data/                  # Armazenamento de dados
│   └── dados.csv          # Base de dados (criada automaticamente)
│
├── docs/                  # Documentação complementar
│   └── .env.example       # Exemplo de variáveis de ambiente
│
└── tests/                 # Testes da aplicação
    └── test_app.py        # Validação de funcionalidades
```

## 📋 Funcionalidades

### Navegação
A aplicação possui navegação automática (multi-página) do Streamlit:
- **Home** - Preenchimento e gerenciamento de solicitações
- **Indicadores** - Dashboard com análises e gráficos
- **Sobre** - Informações sobre o projeto

### Página Home (Preenchimento)
- ✅ Formulário com 8 campos obrigatórios (validados)
- ✅ Seleção de opções predefinidas (Leito, Médico, Recepcionista)
- ✅ Data em formato DD/MM/YYYY
- ✅ Persistência de dados em CSV
- ✅ Tabela com histórico de solicitações
- ✅ Filtros avançados por período, cidade, especialidade
- ✅ Ações: Editar, Duplicar, Deletar
- ✅ Export para CSV

### Página Indicadores (Dashboard)
- ✅ 4 KPI Cards com métricas principais
- ✅ 6 Gráficos interativos (Plotly)
- ✅ Filtros por período
- ✅ Análises por especialidade, hospital, cidade
- ✅ Gerador de relatórios customizados

### Página Sobre
- ✅ Informações sobre o projeto
- ✅ Documentação de funcionalidades
- ✅ Estatísticas gerais do sistema

## 🧪 Testes

Executar validação da instalação:
```bash
python tests/test_app.py
```

## 📊 Dados

Todos os dados são armazenados em: `data/dados.csv`

Estrutura: ID, Data, Nome Paciente, Cidade, Hospital, Solicitante, Diagnóstico, Leito, Especialidade, Aceito, Médico, Recepcionista, Código Justificativa, Data Criação, Data Atualização

## 🔧 Customização

Editar `utils/constants.py` para adicionar:
- Cidades
- Médicos
- Recepcionistas
- Leitos
- Diagnósticos
- Especialidades

## ⚙️ Requisitos

- Python 3.8+
- Streamlit 1.28.0+
- Pandas 2.0.0+
- Plotly 5.14.0+
- Python-dateutil 2.8.2+

## 📝 Como Usar

1. **Registrar Solicitação**: Preencher formulário na página Home
2. **Visualizar Histórico**: Tabela com dados registrados
3. **Filtrar Dados**: Usar filtros para buscar solicitações específicas
4. **Analisar Dados**: Ir para Indicadores para ver gráficos
5. **Exportar Dados**: Baixar CSV com as solicitações

## 📞 Suporte

Para dúvidas ou problemas, verificar:
- Logs da aplicação no terminal
- Arquivo `data/dados.csv` para validar dados
- Executar `python tests/test_app.py` para diagnosticar

---

**Versão**: 1.0 | **Atualizado**: Dezembro de 2025
- [ ] Histórico de modificações (audit log)
- [ ] Integração com bancos de dados reais
- [ ] Modo offline com sincronização
- [ ] Aplicativo mobile
- [ ] API REST
- [ ] Dashboard em tempo real
- [ ] Notificações de email
- [ ] Integração com sistemas de hospital

---

## 💡 Dicas e Boas Práticas

### ✅ Validação de Dados

O sistema valida automaticamente:
- ✓ Nome do paciente (mínimo 3 caracteres, apenas letras)
- ✓ Número de leito (deve ser positivo)
- ✓ Campos obrigatórios
- ✓ Formato de datas

### 📈 Melhor Performance

- Use filtros para reduzir dados exibidos
- Faça backups regularmente
- Limpe dados antigos se arquivo ficar grande

### 🔒 Segurança

- Os dados ficam locais no seu computador
- Não há transmissão para servidores
- Sempre faça backups importantes

---

## 📞 Suporte e Contato

Para dúvidas, sugestões ou reportar bugs:

- **Email:** suporte@susfacil.com
- **Issues:** Abra uma issue no repositório
- **Documentação:** Consulte este README

---

## 📜 Licença

Este projeto é fornecido como está para fins educacionais e operacionais.

---

## 👥 Contribuidores

Desenvolvido com ❤️ para melhorar o gerenciamento de solicitações hospitalares.

---

## 🎉 Changelog

### v1.0 (Dezembro 2025)
- ✅ Lançamento inicial
- ✅ Formulário completo
- ✅ Filtros avançados
- ✅ Dashboard com gráficos
- ✅ Exportação de dados
- ✅ Backup automático

---

**Última atualização:** Dezembro 26, 2025
