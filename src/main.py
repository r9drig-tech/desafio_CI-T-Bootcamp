"""
main.py
Orquestrador principal do pipeline.
Bootcamp CI&T — Do Prompt ao Agente

Uso:
    python src/main.py --pipeline full
    python src/main.py --pipeline ingestion
    python src/main.py --pipeline transformation
    python src/main.py --pipeline agents
"""

import argparse
from dotenv import load_dotenv

load_dotenv()


def run_ingestion():
    from src.ingestion.api_extractor import APIExtractor
    from src.ingestion.csv_loader import CSVLoader

    print("\n📥 [1/5] INGESTÃO DE DADOS")
    extractor = APIExtractor(
        base_url="https://api.bcb.gov.br/dados/serie",
        endpoint="/bcdata.sgs.1/dados",
        params={"formato": "json", "dataInicial": "01/01/2024"},
    )
    return extractor.extract()


def run_transformation(df):
    from src.transformation.cleaner import DataCleaner
    from src.transformation.transformer import DataTransformer

    print("\n🔧 [2/5] LIMPEZA E TRANSFORMAÇÃO")
    df_clean = (
        DataCleaner(df)
        .remove_duplicates()
        .fill_nulls(strategy="median")
        .normalize_dates()
        .get_result()
    )
    df_transformed = (
        DataTransformer(df_clean)
        .get_result()
    )
    return df_transformed


def run_ml(df):
    from src.transformation.feature_eng import FeatureEngineer
    from src.ai.ml_pipeline import MLPipeline

    print("\n🤖 [3/5] MACHINE LEARNING")
    # Ajuste colunas conforme seu dataset real
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) < 2:
        print("⚠️  Dataset sem colunas numéricas suficientes para ML. Pulando.")
        return

    target = numeric_cols[-1]
    fe = FeatureEngineer(df[numeric_cols].dropna())
    X_train, X_test, y_train, y_test = fe.split(target_col=target)

    pipeline = MLPipeline(task="regression")
    pipeline.train(X_train, y_train, algorithm="random_forest")
    pipeline.evaluate(X_test, y_test)
    pipeline.feature_importance()
    pipeline.save("models/model.pkl")


def run_agents(df):
    from src.agents.insight_agent import InsightAgent
    from src.agents.report_agent import ReportAgent

    print("\n💡 [4/5] GERAÇÃO DE INSIGHTS COM IA")
    insight = InsightAgent()
    summary = insight.run(df, context="Dados do Banco Central do Brasil 2024",
                          output="executive_summary")
    print(summary)

    print("\n📄 [5/5] GERAÇÃO DE RELATÓRIO AUTOMÁTICO")
    reporter = ReportAgent()
    reporter.generate(
        df=df,
        title="Relatório Automático — Pipeline CI&T",
        context="Dados extraídos da API do Banco Central do Brasil.",
        output_path="reports/relatorio_automatico.md",
    )


def main():
    parser = argparse.ArgumentParser(description="Pipeline de Dados para IA — CI&T Bootcamp")
    parser.add_argument(
        "--pipeline",
        choices=["full", "ingestion", "transformation", "agents"],
        default="full",
        help="Etapa do pipeline a executar",
    )
    args = parser.parse_args()

    print("🚀 Pipeline de Dados para IA — CI&T Bootcamp")
    print("=" * 50)

    if args.pipeline in ("ingestion", "full"):
        df = run_ingestion()

    if args.pipeline in ("transformation", "full"):
        if args.pipeline == "transformation":
            df = run_ingestion()
        df = run_transformation(df)

    if args.pipeline == "full":
        run_ml(df)
        run_agents(df)

    if args.pipeline == "agents":
        df = run_ingestion()
        df = run_transformation(df)
        run_agents(df)

    print("\n✅ Pipeline concluído com sucesso!")


if __name__ == "__main__":
    main()
