<!-- START_SECTION:header -->
<div align="center">
  <img alt="DIO Education" src="https://raw.githubusercontent.com/digitalinnovationone/template-github-trilha/main/.github/assets/logo.webp" width="100px" />
  <h1>🚀 Desafio CI&T - Do Prompt ao Agente</h1>   
</div>
<!--END_SECTION:header-->

<p align="center">
  <img src="https://img.shields.io/static/v1?label=CI%26T&message=Bootcamp&color=E94D5F&labelColor=202024" alt="CI&T Bootcamp" />
  <img src="https://img.shields.io/static/v1?label=Nivel&message=Basico&color=E94D5F&labelColor=202024" alt="Nivel" />
  <img src="https://img.shields.io/static/v1?label=Status&message=Em%20Desenvolvimento&color=00B37E&labelColor=202024" alt="Status" />
  <img src="https://img.shields.io/static/v1?label=AI%20Agents&message=Basico&color=E94D5F&labelColor=202024" alt="IA" />
  <img src="https://img.shields.io/static/v1?label=Python&message=3.11%2B&color=3776AB&labelColor=202024&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/static/v1?label=Power%20BI&message=Dashboard&color=F2C811&labelColor=202024" alt="Power BI" />
  
</p>

---

<!--  -->
<table align="center">
  <thead>
    <tr>
      <td>
        <a href="https://github.com/r9drig-tech">
          <img src="https://github.com/r9drig-tech.png" width="115px" alt="@r9drig-tech"><br>
        </a>
      </td>
      <td colspan="3">
        <h3>Rodrigo Salgado</h3>
        <p>
          🎉 10y+ de experiência em Business Intelligence e Dashboards com Power BI.<br/>
          🌟 Analista BI & Dados — Estudante de Engenharia de Dados & IA<br/>
          👨‍💻 Foco em Data Analytics, Power BI e Inteligência Artificial
        </p>
        <a href="https://www.linkedin.com/in/r9drig-power-bi/" align="center">
          <img align="center" alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white">
        </a>
        &nbsp;
        <a href="https://github.com/r9drig-tech">
          <img align="center" alt="GitHub" src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white">
        </a>
      </td>
    </tr>
  </thead>
</table>
<!--  -->

<br/>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Sobre o Bootcamp](#-sobre-o-bootcamp-cit--do-prompt-ao-agente)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos-de-habilidades)
- [Habilidades Desenvolvidas](#-habilidades-desenvolvidas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Executar](#-como-executar)
- [Etapas do Pipeline](#-etapas-do-pipeline)
- [Dashboard Power BI](#-dashboard-power-bi)
- [Objetivos e Resultados](#-objetivos-e-resultados-esperados)
- [Roadmap](#-roadmap)

---

## 💻 Sobre o Projeto

Este projeto foi desenvolvido durante o **Bootcamp CI&T — Do Prompt ao Agente** e consiste em construir um **pipeline de dados end-to-end voltado para Inteligência Artificial**.

O objetivo é preparar dados brutos, realizar transformações e disponibilizá-los para modelos de Machine Learning e dashboards analíticos — combinando **Engenharia de Dados moderna** com **IA generativa** e **agentes inteligentes**.

### O projeto inclui:

| Etapa | Descrição |
|-------|-----------|
| 📥 **Ingestão** | Coleta de dados de múltiplas fontes (CSV, APIs, bancos de dados) |
| 🔧 **Processamento** | Limpeza, validação e transformação dos dados |
| 🏛️ **Armazenamento** | Data Lake e Data Warehouse com modelagem dimensional |
| 🤖 **Agentes de IA** | Análise autônoma, insights e relatórios automáticos com LLMs |
| 📊 **Visualização** | Dashboards interativos e inteligentes no Power BI |

---

## 🏢 Sobre o Bootcamp CI&T — Do Prompt ao Agente

O **CI&T Bootcamp** é um programa intensivo de capacitação em **IA aplicada à Engenharia de Dados**, conduzido pela [CI&T](https://ciandt.com/br), empresa global de tecnologia e transformação digital.

> *"Do Prompt ao Agente"* — aprenda a usar IA generativa e agentes inteligentes para automatizar e escalar pipelines de dados em ambientes corporativos reais.

**O que o bootcamp cobre:**
- Fundamentos de IA generativa e Prompt Engineering avançado
- Construção de agentes de IA com LangChain e OpenAI
- Engenharia de Dados com Python, SQL e Cloud
- Integração de LLMs em pipelines de dados
- Dashboards inteligentes conectados a agentes de IA

---

## 🏗️ Arquitetura

```
┌──────────────────────────────────────────────────────────────┐
│                     FONTES DE DADOS                          │
│    [CSV / Excel]    [APIs Públicas]    [Banco de Dados]      │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                   CAMADA DE INGESTÃO                         │
│               Python + Apache Airflow                        │
│           (Extração, Validação, Staging)                     │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                 DATA LAKE  (Raw Zone)                        │
│              Dados brutos preservados                        │
│               (Azure Blob / GCS / S3)                        │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│          CAMADA DE TRANSFORMAÇÃO — ETL/ELT                   │
│       Python (Pandas / PySpark) + dbt Core                   │
│    (Limpeza, Normalização, Modelagem Dimensional)            │
└──────────────┬─────────────────────────┬─────────────────────┘
               │                         │
               ▼                         ▼
┌──────────────────────┐    ┌────────────────────────────────────┐
│  AGENTES DE IA 🤖    │    │    DATA WAREHOUSE (Curated)        │
│                      │    │  PostgreSQL / BigQuery             │
│  • LangChain Agents  │    │  Star Schema — Fato + Dimensões    │
│  • OpenAI GPT-4o     │    └──────────────┬─────────────────────┘
│  • Scikit-learn      │                   │
│  • TensorFlow        │                   ▼
│  • Insight Agent     │    ┌────────────────────────────────────┐
│  • Report Agent      │    │     POWER BI DASHBOARD 📊          │
└──────────────────────┘    │  Relatórios + Narrativas por IA    │
                            │  Atualização automática            │
                            └────────────────────────────────────┘
```

---

## 🛠️ Tecnologias

### Core Stack

| Tecnologia | Uso |
|------------|-----|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Pipeline principal, ETL, automação |
| ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) | Manipulação e transformação de dados |
| ![Apache Spark](https://img.shields.io/badge/PySpark-E25A1C?style=flat&logo=apachespark&logoColor=white) | Processamento distribuído |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white) | Data Warehouse relacional |
| ![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=powerbi&logoColor=black) | Dashboards e visualização |

### IA & Agentes

| Tecnologia | Uso |
|------------|-----|
| ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white) | LLMs, GPT-4o, geração de insights |
| LangChain | Construção de agentes de IA autônomos |
| Scikit-learn | Modelos de Machine Learning |
| TensorFlow | Deep Learning |

### Infraestrutura

| Tecnologia | Uso |
|------------|-----|
| Apache Airflow | Orquestração e agendamento do pipeline |
| dbt Core | Transformação e modelagem de dados |
| Docker | Containerização dos serviços |
| GitHub Actions | CI/CD automatizado |
| Azure / GCP | Cloud Storage e processamento |

---

## 📚 Pré-requisitos de Habilidades

Antes de ingressar neste conteúdo, é necessário possuir conhecimento prévio nas seguintes áreas:

| Habilidade | Nível Necessário |
|------------|-----------------|
| SQL (JOINs, CTEs, Window Functions) | ⭐⭐⭐ Intermediário |
| Python (Pandas, funções, OOP básico) | ⭐⭐⭐ Intermediário |
| Lógica de Programação | ⭐⭐ Básico |
| Estatística Descritiva | ⭐⭐ Básico |
| Power BI (modelagem, DAX básico) | ⭐⭐⭐ Intermediário |

---

## 🧠 Habilidades Desenvolvidas

### Engenharia de Dados
- ✅ ETL com Python (Pandas + PySpark)
- ✅ Spark e Databricks para processamento distribuído
- ✅ Modelagem relacional e dimensional (Star Schema)
- ✅ Consultas SQL avançadas (CTEs, Window Functions)
- ✅ Orquestração com Apache Airflow
- ✅ Transformações com dbt Core

### Inteligência Artificial & Agentes
- ✅ Fundamentos de IA generativa e Prompt Engineering
- ✅ Construção de Agentes autônomos com LangChain + OpenAI
- ✅ Preparação de datasets para Machine Learning
- ✅ Integração com Scikit-learn e TensorFlow
- ✅ Geração automática de insights em linguagem natural

### Visualização
- ✅ Dashboards interativos no Power BI
- ✅ Power BI conectado a pipelines em tempo real
- ✅ Narrativas automáticas geradas por agentes de IA

---

## 📁 Estrutura do Projeto

```
pipeline-dados-ia/
│
├── 📂 data/
│   ├── raw/                      # Dados brutos
│   ├── processed/                # Dados transformados
│   └── datasets/                 # Datasets prontos para ML
│
├── 📂 src/
│   ├── ingestion/
│   │   ├── api_extractor.py      # Extração de APIs públicas
│   │   ├── csv_loader.py         # Carregamento de CSV/Excel
│   │   └── db_connector.py       # Conexão com bancos
│   │
│   ├── transformation/
│   │   ├── cleaner.py            # Limpeza e validação
│   │   ├── transformer.py        # Transformações
│   │   └── feature_eng.py        # Feature Engineering para ML
│   │
│   ├── agents/
│   │   ├── data_agent.py         # Agente de análise de dados
│   │   ├── insight_agent.py      # Agente gerador de insights
│   │   └── report_agent.py       # Agente de relatórios automáticos
│   │
│   └── ai/
│       ├── ml_pipeline.py        # Pipeline de Machine Learning
│       └── llm_integration.py    # Integração com LLMs
│
├── 📂 dbt/models/
│   ├── staging/                  # Raw → limpo
│   ├── intermediate/             # Transformações intermediárias
│   └── marts/                    # Fato + Dimensões
│
├── 📂 airflow/dags/
│   └── pipeline_dag.py           # DAG principal
│
├── 📂 powerbi/
│   └── dashboard.pbix            # Dashboard Power BI
│
├── 📂 notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_ml_experiments.ipynb
│   └── 05_agents_demo.ipynb
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## ▶️ Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/r9drig-tech/pipeline-dados-ia.git
cd pipeline-dados-ia
```

### 2. Configure o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env com suas credenciais
```

```env
OPENAI_API_KEY=sua_chave_aqui
DB_HOST=localhost
DB_PORT=5432
DB_NAME=data_warehouse
DB_USER=usuario
DB_PASSWORD=senha
```

### 4. Suba os serviços

```bash
docker-compose up -d
```

### 5. Execute o pipeline

```bash
# Pipeline completo
python src/main.py --pipeline full

# Apenas ingestão
python src/main.py --pipeline ingestion

# Apenas agentes de IA
python src/main.py --pipeline agents
```

---

## 📊 Etapas do Pipeline

### Etapa 1 — Ingestão de Dados

```python
from src.ingestion.api_extractor import APIExtractor

extractor = APIExtractor(
    base_url="https://api.bcb.gov.br/dados/serie",
    endpoint="/bcdata.sgs.1/dados"
)
df = extractor.extract()
print(f"✅ {len(df)} registros extraídos!")
```

### Etapa 2 — Limpeza e Transformação

```python
from src.transformation.cleaner import DataCleaner

df_clean = (DataCleaner(df)
    .remove_duplicates()
    .fill_nulls(strategy="median")
    .normalize_dates()
    .get_result())

print(f"📊 Qualidade dos dados: {cleaner.quality_score:.1%}")
```

### Etapa 3 — Agente de Insights com IA

```python
from src.agents.insight_agent import InsightAgent

agent = InsightAgent(model="gpt-4o")
insights = agent.run(
    data=df_clean,
    context="Indicadores econômicos brasileiros 2024",
    output="executive_summary"
)
print(insights)
# → "Os dados revelam crescimento de 3.2% no Q3, com destaque para..."
```

---

## 📈 Dashboard Power BI

O dashboard está conectado diretamente ao Data Warehouse e inclui **narrativas geradas automaticamente por agentes de IA**:

| Página | Descrição |
|--------|-----------|
| 🏠 Overview | KPIs principais + resumo executivo gerado por IA |
| 📊 Análise Temporal | Tendências e sazonalidade |
| 🤖 Insights do Agente | Narrativas automáticas em linguagem natural |
| ⚙️ Pipeline Status | Monitoramento em tempo real |

---

## 🎯 Objetivos e Resultados Esperados

Após a conclusão do projeto, estarei apto a:

- ✅ Construir pipelines de dados escaláveis para IA
- ✅ Integrar múltiplas fontes de dados em ambientes de nuvem
- ✅ Criar e orquestrar **agentes de IA** sobre dados reais
- ✅ Preparar datasets para treinamento de modelos de Machine Learning
- ✅ Criar dashboards conectados a pipelines e enriquecidos com IA
- ✅ Documentar e apresentar soluções de dados voltadas para IA

---

## 🗺️ Roadmap

- [x] Estrutura base do projeto
- [x] Pipeline de ingestão (CSV + API)
- [x] Camada de limpeza e transformação
- [ ] Modelagem dimensional no Data Warehouse
- [ ] Integração com PySpark / Databricks
- [ ] Agente de análise de dados com LangChain
- [ ] Agente gerador de insights automáticos
- [ ] Dashboard Power BI completo com narrativas IA
- [ ] Orquestração com Airflow
- [ ] Deploy em Cloud (Azure / GCP)
- [ ] CI/CD com GitHub Actions

---

<!--START_SECTION:footer-->
<br />
<br />
<p align="center">
  Desenvolvido durante o <strong>Bootcamp CI&T — Do Prompt ao Agente</strong><br/>
  por <a href="https://github.com/r9drig-tech">Rodrigo Salgado</a> 🚀
</p>
<!--END_SECTION:footer-->
