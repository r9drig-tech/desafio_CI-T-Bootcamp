"""
pipeline_dag.py
DAG principal do pipeline de dados para IA.
Bootcamp CI&T — Do Prompt ao Agente
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# ── Configurações padrão ─────────────────────────────────────────────────────
default_args = {
    "owner":            "rodrigo.salgado",
    "depends_on_past":  False,
    "start_date":       datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry":   False,
    "retries":          2,
    "retry_delay":      timedelta(minutes=5),
}

# ── Funções de cada etapa ────────────────────────────────────────────────────

def task_ingestao(**context):
    """Extrai dados da API do Banco Central."""
    import sys
    sys.path.append('/opt/airflow/dags/pipeline-dados-ia')
    from src.ingestion.api_extractor import APIExtractor

    extractor = APIExtractor(
        base_url="https://api.bcb.gov.br/dados/serie",
        endpoint="/bcdata.sgs.1/dados",
        params={"formato": "json", "dataInicial": "01/01/2024"},
    )
    df = extractor.extract()

    # Salva para o próximo step via XCom
    context["ti"].xcom_push(key="raw_shape", value=str(df.shape))
    df.to_csv("/tmp/dados_raw.csv", index=False)
    print(f"✅ Ingestão concluída: {df.shape}")


def task_limpeza(**context):
    """Limpeza e validação dos dados brutos."""
    import pandas as pd
    import sys
    sys.path.append('/opt/airflow/dags/pipeline-dados-ia')
    from src.transformation.cleaner import DataCleaner

    df = pd.read_csv("/tmp/dados_raw.csv")
    df_clean = (
        DataCleaner(df)
        .remove_duplicates()
        .fill_nulls(strategy="median")
        .normalize_dates()
        .get_result()
    )
    df_clean.to_csv("/tmp/dados_clean.csv", index=False)
    print(f"✅ Limpeza concluída: {df_clean.shape}")


def task_transformacao(**context):
    """Transformações e enriquecimento dos dados."""
    import pandas as pd
    import sys
    sys.path.append('/opt/airflow/dags/pipeline-dados-ia')
    from src.transformation.transformer import DataTransformer

    df = pd.read_csv("/tmp/dados_clean.csv")
    df_t = DataTransformer(df).get_result()
    df_t.to_csv("/tmp/dados_transformed.csv", index=False)
    print(f"✅ Transformação concluída: {df_t.shape}")


def task_carga(**context):
    """Carrega dados no Data Warehouse."""
    import pandas as pd
    import sys
    sys.path.append('/opt/airflow/dags/pipeline-dados-ia')
    from src.ingestion.db_connector import DBConnector

    df = pd.read_csv("/tmp/dados_transformed.csv")
    db = DBConnector()
    db.write(df, table="fato_indicadores", if_exists="append")
    db.close()
    print(f"✅ Carga concluída: {len(df)} registros")


def task_insights(**context):
    """Gera insights automáticos com IA."""
    import pandas as pd
    import sys
    sys.path.append('/opt/airflow/dags/pipeline-dados-ia')
    from src.agents.insight_agent import InsightAgent

    df = pd.read_csv("/tmp/dados_transformed.csv")
    agent = InsightAgent()
    insight = agent.run(
        df,
        context="Indicadores econômicos brasileiros",
        output="executive_summary"
    )
    print(f"✅ Insights gerados:\n{insight}")


# ── Definição da DAG ─────────────────────────────────────────────────────────
with DAG(
    dag_id="pipeline_dados_ia",
    default_args=default_args,
    description="Pipeline de Dados para IA — CI&T Bootcamp",
    schedule_interval="0 6 * * *",   # Todo dia às 6h
    catchup=False,
    tags=["ci&t", "dados", "ia", "pipeline"],
) as dag:

    t1_ingestao = PythonOperator(
        task_id="ingestao_api",
        python_callable=task_ingestao,
    )

    t2_limpeza = PythonOperator(
        task_id="limpeza_validacao",
        python_callable=task_limpeza,
    )

    t3_transformacao = PythonOperator(
        task_id="transformacao_enriquecimento",
        python_callable=task_transformacao,
    )

    t4_dbt = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dags/pipeline-dados-ia/dbt && dbt run --profiles-dir .",
    )

    t5_carga = PythonOperator(
        task_id="carga_warehouse",
        python_callable=task_carga,
    )

    t6_insights = PythonOperator(
        task_id="geracao_insights_ia",
        python_callable=task_insights,
    )

    # ── Fluxo da DAG ──────────────────────────────────────────────────────────
    t1_ingestao >> t2_limpeza >> t3_transformacao >> t4_dbt >> t5_carga >> t6_insights
