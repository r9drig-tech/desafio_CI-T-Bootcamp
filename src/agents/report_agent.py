"""
report_agent.py
Agente gerador de relatórios automáticos em Markdown.
Bootcamp CI&T — Do Prompt ao Agente
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from openai import OpenAI

from src.agents.insight_agent import InsightAgent


class ReportAgent:
    """
    Gera relatórios completos em Markdown a partir de um DataFrame.
    Combina análise estatística + insights gerados por IA.
    """

    def __init__(self, model: str = "gpt-4o"):
        self.client        = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model         = model
        self.insight_agent = InsightAgent(model=model)

    # ── Seções do relatório ──────────────────────────────────────────────────

    def _header(self, title: str, context: str) -> str:
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        return (
            f"# 📊 {title}\n\n"
            f"> **Gerado automaticamente pelo ReportAgent — CI&T Bootcamp**  \n"
            f"> 🤖 Modelo: `{self.model}` | 📅 {now}\n\n"
            f"---\n\n"
            f"## 🎯 Contexto\n\n{context}\n\n---\n\n"
        )

    def _overview_section(self, df: pd.DataFrame) -> str:
        numeric = df.select_dtypes(include="number")
        return (
            f"## 📋 Visão Geral do Dataset\n\n"
            f"| Atributo | Valor |\n"
            f"|----------|-------|\n"
            f"| Total de registros | {len(df):,} |\n"
            f"| Total de colunas   | {len(df.columns)} |\n"
            f"| Colunas numéricas  | {len(numeric.columns)} |\n"
            f"| Valores nulos      | {df.isnull().sum().sum():,} |\n"
            f"| Período (se datas) | {self._detect_period(df)} |\n\n"
        )

    def _detect_period(self, df: pd.DataFrame) -> str:
        date_cols = [c for c in df.columns if "data" in c or "date" in c or "mes" in c]
        if not date_cols:
            return "N/A"
        col = df[date_cols[0]]
        return f"{col.min()} → {col.max()}"

    def _stats_section(self, df: pd.DataFrame) -> str:
        numeric = df.select_dtypes(include="number")
        if numeric.empty:
            return ""
        stats = numeric.describe().round(2)
        md_table = stats.to_markdown() if hasattr(stats, "to_markdown") else str(stats)
        return f"## 📈 Estatísticas Descritivas\n\n{md_table}\n\n"

    def _insights_section(self, df: pd.DataFrame, context: str) -> str:
        bullets = self.insight_agent.run(df, context, output="bullet_points")
        return f"## 💡 Insights Gerados por IA\n\n{bullets}\n\n"

    def _executive_section(self, df: pd.DataFrame, context: str) -> str:
        summary = self.insight_agent.run(df, context, output="executive_summary")
        return f"## 📝 Resumo Executivo\n\n{summary}\n\n"

    def _recommendations_section(self, df: pd.DataFrame, context: str) -> str:
        json_str = self.insight_agent.run(df, context, output="json")
        try:
            data = json.loads(json_str)
            recs = data.get("recomendacoes", [])
            alerts = data.get("alertas", [])
        except Exception:
            return ""

        rec_md  = "\n".join(f"- {r}" for r in recs)
        alert_md = "\n".join(f"- ⚠️ {a}" for a in alerts)
        return (
            f"## 🚀 Recomendações\n\n{rec_md}\n\n"
            f"## ⚠️ Alertas\n\n{alert_md}\n\n"
        )

    def _footer(self) -> str:
        return (
            "\n---\n\n"
            "*Relatório gerado automaticamente pelo **ReportAgent** — "
            "Bootcamp CI&T — Do Prompt ao Agente* 🤖\n"
        )

    # ── Método principal ─────────────────────────────────────────────────────

    def generate(self, df: pd.DataFrame, title: str, context: str,
                 output_path: Optional[str] = None) -> str:
        """
        Gera o relatório completo em Markdown.

        Args:
            df:          DataFrame com os dados
            title:       Título do relatório
            context:     Contexto do negócio
            output_path: Caminho para salvar o .md (opcional)

        Returns:
            String com o relatório em Markdown
        """
        print(f"📄 Gerando relatório: '{title}'...")

        report = (
            self._header(title, context)
            + self._overview_section(df)
            + self._stats_section(df)
            + self._executive_section(df, context)
            + self._insights_section(df, context)
            + self._recommendations_section(df, context)
            + self._footer()
        )

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_text(report, encoding="utf-8")
            print(f"✅ Relatório salvo em: {output_path}")

        return report


# ── Exemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import numpy as np

    df = pd.DataFrame({
        "mes":      pd.period_range("2024-01", periods=12, freq="M").astype(str),
        "vendas":   [520, 310, 280, 190, 140, 220, 175, 130, 160, 145, 90, 85],
        "meta":     [500, 300, 250, 180, 150, 200, 170, 120, 155, 140, 100, 90],
        "clientes": [1200, 800, 700, 500, 380, 580, 460, 340, 420, 380, 240, 220],
    })

    agent = ReportAgent()
    report = agent.generate(
        df=df,
        title="Relatório Comercial — 2024",
        context="Análise do desempenho de vendas mensais vs metas corporativas.",
        output_path="reports/relatorio_comercial_2024.md",
    )
    print(report[:500])  # Preview
