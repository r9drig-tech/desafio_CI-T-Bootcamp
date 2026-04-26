"""
cleaner.py
Limpeza e validação de dados.
Bootcamp CI&T — Do Prompt ao Agente
"""

import pandas as pd
import numpy as np
from typing import List, Optional


class DataCleaner:
    """Pipeline fluente de limpeza e validação de DataFrames."""

    def __init__(self, df: pd.DataFrame):
        self._df = df.copy()
        self._log: List[str] = []

    # ── Limpeza ─────────────────────────────────────────────────────────────

    def remove_duplicates(self, subset: Optional[List[str]] = None) -> "DataCleaner":
        before = len(self._df)
        self._df = self._df.drop_duplicates(subset=subset)
        removed = before - len(self._df)
        self._log.append(f"remove_duplicates: {removed} linhas removidas")
        return self

    def fill_nulls(self, strategy: str = "median",
                   fill_value=None, columns: Optional[List[str]] = None) -> "DataCleaner":
        """Preenche nulos. strategy: 'median' | 'mean' | 'mode' | 'value'"""
        cols = columns or self._df.select_dtypes(include=[np.number]).columns.tolist()
        for col in cols:
            if col not in self._df.columns:
                continue
            if strategy == "median":
                val = self._df[col].median()
            elif strategy == "mean":
                val = self._df[col].mean()
            elif strategy == "mode":
                val = self._df[col].mode()[0]
            else:
                val = fill_value
            self._df[col] = self._df[col].fillna(val)
        self._log.append(f"fill_nulls: strategy='{strategy}' em {len(cols)} colunas")
        return self

    def normalize_dates(self, columns: Optional[List[str]] = None,
                        fmt: str = "%Y-%m-%d") -> "DataCleaner":
        """Converte colunas de data para datetime."""
        cols = columns or [c for c in self._df.columns if "data" in c or "date" in c]
        for col in cols:
            if col in self._df.columns:
                self._df[col] = pd.to_datetime(self._df[col], errors="coerce")
        self._log.append(f"normalize_dates: {cols}")
        return self

    def remove_outliers(self, columns: Optional[List[str]] = None,
                        method: str = "iqr") -> "DataCleaner":
        """Remove outliers pelo método IQR."""
        cols = columns or self._df.select_dtypes(include=[np.number]).columns.tolist()
        before = len(self._df)
        for col in cols:
            if col not in self._df.columns:
                continue
            Q1 = self._df[col].quantile(0.25)
            Q3 = self._df[col].quantile(0.75)
            IQR = Q3 - Q1
            self._df = self._df[
                (self._df[col] >= Q1 - 1.5 * IQR) &
                (self._df[col] <= Q3 + 1.5 * IQR)
            ]
        self._log.append(f"remove_outliers: {before - len(self._df)} linhas removidas")
        return self

    def validate_schema(self, expected_columns: List[str]) -> "DataCleaner":
        """Verifica se colunas obrigatórias existem."""
        missing = [c for c in expected_columns if c not in self._df.columns]
        if missing:
            raise ValueError(f"❌ Colunas ausentes: {missing}")
        self._log.append(f"validate_schema: OK ({len(expected_columns)} colunas)")
        return self

    # ── Resultado ───────────────────────────────────────────────────────────

    @property
    def quality_score(self) -> float:
        """Percentual de células preenchidas (sem nulos)."""
        total = self._df.size
        nulls = self._df.isnull().sum().sum()
        return (total - nulls) / total if total > 0 else 0.0

    def get_result(self) -> pd.DataFrame:
        print("\n📋 Log de limpeza:")
        for step in self._log:
            print(f"  ▸ {step}")
        print(f"  ▸ quality_score: {self.quality_score:.1%}")
        print(f"  ▸ shape final: {self._df.shape}")
        return self._df


# ── Exemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    df_raw = pd.DataFrame({
        "data":  ["2024-01-01", "2024-01-02", None, "2024-01-01"],
        "valor": [100, None, 300, 100],
        "regiao": ["SP", "RJ", "MG", "SP"],
    })

    df_clean = (
        DataCleaner(df_raw)
        .remove_duplicates()
        .fill_nulls(strategy="median")
        .normalize_dates()
        .validate_schema(["data", "valor", "regiao"])
        .get_result()
    )
    print(df_clean)
