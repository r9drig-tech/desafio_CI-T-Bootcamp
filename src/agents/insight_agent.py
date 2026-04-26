"""
insight_agent.py
Agente gerador de insights automáticos em linguagem natural.
Bootcamp CI&T — Do Prompt ao Agente
"""

import os
import json
import pandas as pd
from openai import OpenAI
from typing import Literal


OutputFormat = Literal["executive_summary", "bullet_points", "narrative", "json"]


class InsightAgent:
    """
    Gera insights automáticos sobre um DataFrame usando a OpenAI API.
    Não requer LangChain — usa a API diretamente para máxima simplicidade.
    """

    PROMPTS = {
        "executive_summary": (
            "Você é um analista de dados sênior. Com base no resumo estatístico abaixo, "
            "escreva um parágrafo executivo (5-7 linhas) destacando os principais achados, "
            "tendências relevantes e alertas. Seja direto e objetivo. Responda em português."
        ),
        "bullet_points": (
            "Você é um analista de dados. Com base nos dados abaixo, liste de 5 a 8 insights "
            "relevantes em formato de bullet points. Inclua números e percentuais quando possível. "
            "Responda em português."
        ),
        "narrative": (
            "Você é um storyteller de dados. Com base nos dados abaixo, crie uma narrativa "
            "fluida de 3 parágrafos: contexto, descoberta principal e recomendação. "
            "Responda em português."
        ),
        "json": (
            "Você é um analista de dados. Com base nos dados abaixo, retorne um JSON com as "
            'chaves: "resumo" (string), "principais_metricas" (dict), "alertas" (list), '
            '"recomendacoes" (list). Retorne APENAS o JSON, sem markdown.'
        ),
    }

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.4):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature

    def _build_data_summary(self, df: pd.DataFrame, context: str) -> str:
        """Cria um resumo textual do DataFrame para enviar ao modelo."""
        numeric_cols = df.select_dtypes(include="number")
        cat_cols     = df.select_dtypes(include=["object", "category"])

        summary_parts = [
            f"Contexto: {context}",
            f"Shape: {df.shape[0]} linhas × {df.shape[1]} colunas",
            f"Colunas: {df.columns.tolist()}",
            f"Nulos por coluna: {df.isnull().sum().to_dict()}",
        ]

        if not numeric_cols.empty:
            summary_parts.append(
                f"Estatísticas numéricas:\n{numeric_cols.describe().round(2).to_string()}"
            )

        if not cat_cols.empty:
            for col in cat_cols.columns[:3]:  # Limita a 3 colunas categóricas
                top = df[col].value_counts().head(5).to_dict()
                summary_parts.append(f"Top valores em '{col}': {top}")

        return "\n\n".join(summary_parts)

    def run(self, df: pd.DataFrame, context: str = "Análise de dados",
            output: OutputFormat = "executive_summary") -> str:
        """
        Gera insights sobre o DataFrame.

        Args:
            df:      DataFrame com os dados
            context: Descrição do negócio/contexto dos dados
            output:  Formato de saída desejado

        Returns:
            String com o insight gerado (ou JSON string se output='json')
        """
        system_prompt = self.PROMPTS.get(output, self.PROMPTS["executive_summary"])
        data_summary  = self._build_data_summary(df, context)

        print(f"🤖 Gerando insights (formato: {output})...")

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": f"Dados para análise:\n\n{data_summary}"},
            ],
        )

        result = response.choices[0].message.content.strip()

        if output == "json":
            try:
                parsed = json.loads(result)
                return json.dumps(parsed, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                return result  # Retorna bruto se não parsear

        return result


# ── Exemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import numpy as np

    df = pd.DataFrame({
        "mes":    pd.period_range("2024-01", periods=12, freq="M").astype(str),
        "regiao": ["SP", "RJ", "MG", "RS", "BA", "PR", "SC", "GO", "PE", "CE", "AM", "PA"],
        "vendas": [520, 310, 280, 190, 140, 220, 175, 130, 160, 145, 90, 85],
        "meta":   [500, 300, 250, 180, 150, 200, 170, 120, 155, 140, 100, 90],
        "clientes": [1200, 800, 700, 500, 380, 580, 460, 340, 420, 380, 240, 220],
    })

    agent = InsightAgent()

    print("=== RESUMO EXECUTIVO ===")
    print(agent.run(df, context="Desempenho comercial regional 2024", output="executive_summary"))

    print("\n=== BULLET POINTS ===")
    print(agent.run(df, context="Desempenho comercial regional 2024", output="bullet_points"))

    print("\n=== JSON ===")
    print(agent.run(df, context="Desempenho comercial regional 2024", output="json"))
