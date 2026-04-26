"""
transformer.py
Transformações, agregações e modelagem dimensional.
Bootcamp CI&T — Do Prompt ao Agente
"""

import pandas as pd
from typing import List, Dict, Optional


class DataTransformer:
    """Transformações e enriquecimentos sobre DataFrames."""

    def __init__(self, df: pd.DataFrame):
        self._df = df.copy()

    def add_date_parts(self, date_col: str) -> "DataTransformer":
        """Extrai ano, mês, dia, trimestre e dia da semana de uma coluna de data."""
        col = pd.to_datetime(self._df[date_col], errors="coerce")
        self._df[f"{date_col}_ano"]       = col.dt.year
        self._df[f"{date_col}_mes"]       = col.dt.month
        self._df[f"{date_col}_dia"]       = col.dt.day
        self._df[f"{date_col}_trimestre"] = col.dt.quarter
        self._df[f"{date_col}_semana"]    = col.dt.isocalendar().week.astype(int)
        self._df[f"{date_col}_dia_semana"]= col.dt.day_name()
        print(f"✅ Partes de data extraídas de '{date_col}'")
        return self

    def rename_columns(self, mapping: Dict[str, str]) -> "DataTransformer":
        self._df = self._df.rename(columns=mapping)
        return self

    def select_columns(self, columns: List[str]) -> "DataTransformer":
        self._df = self._df[columns]
        return self

    def aggregate(self, group_by: List[str], agg: Dict[str, str]) -> "DataTransformer":
        """Agrega o DataFrame. Ex: agg={'valor': 'sum', 'qtd': 'count'}"""
        self._df = self._df.groupby(group_by).agg(agg).reset_index()
        print(f"✅ Agregado por {group_by} → {len(self._df)} grupos")
        return self

    def add_calculated_column(self, col_name: str, formula: str) -> "DataTransformer":
        """Cria coluna via eval. Ex: formula='valor * 1.1'"""
        self._df[col_name] = self._df.eval(formula)
        return self

    def pivot(self, index: str, columns: str, values: str,
              aggfunc: str = "sum") -> "DataTransformer":
        self._df = self._df.pivot_table(
            index=index, columns=columns, values=values, aggfunc=aggfunc
        ).reset_index()
        self._df.columns.name = None
        return self

    def to_star_schema(self, fact_cols: List[str],
                       dim_configs: List[Dict]) -> Dict[str, pd.DataFrame]:
        """
        Desnormaliza o DataFrame em tabelas de fato e dimensões.

        dim_configs: lista de dicts com keys:
          - name:    nome da dimensão (ex: 'dim_regiao')
          - columns: colunas que compõem a dimensão
          - key:     nome da chave surrogate a criar (ex: 'id_regiao')
        """
        tables = {}
        df_fact = self._df[fact_cols].copy()

        for cfg in dim_configs:
            dim_cols = cfg["columns"]
            key_col  = cfg["key"]
            dim_name = cfg["name"]

            dim_df = self._df[dim_cols].drop_duplicates().reset_index(drop=True)
            dim_df[key_col] = dim_df.index + 1          # surrogate key

            # Join da chave de volta ao fato
            df_fact = df_fact.merge(dim_df[[*dim_cols, key_col]], on=dim_cols, how="left")
            df_fact = df_fact.drop(columns=dim_cols)    # remove colunas naturais do fato

            tables[dim_name] = dim_df
            print(f"✅ Dimensão '{dim_name}' criada com {len(dim_df)} registros")

        tables["fato"] = df_fact
        print(f"✅ Tabela fato criada com {len(df_fact)} registros e {len(df_fact.columns)} colunas")
        return tables

    def get_result(self) -> pd.DataFrame:
        return self._df


# ── Exemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = pd.DataFrame({
        "data":   pd.date_range("2024-01-01", periods=6, freq="ME"),
        "regiao": ["SP", "RJ", "SP", "MG", "RJ", "SP"],
        "produto":["A", "B", "A", "C", "B", "C"],
        "valor":  [100, 200, 150, 80, 220, 90],
        "qtd":    [10, 20, 15, 8, 22, 9],
    })

    transformer = DataTransformer(df)
    result = (
        transformer
        .add_date_parts("data")
        .add_calculated_column("receita_total", "valor * qtd")
        .get_result()
    )
    print(result.head())
