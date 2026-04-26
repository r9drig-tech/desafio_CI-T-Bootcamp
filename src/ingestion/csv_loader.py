"""
csv_loader.py
Carregamento de arquivos CSV e Excel.
Bootcamp CI&T — Do Prompt ao Agente
"""

import pandas as pd
from pathlib import Path
from typing import Optional


class CSVLoader:
    """Carrega arquivos CSV ou Excel e retorna um DataFrame padronizado."""

    SUPPORTED = {".csv", ".tsv", ".xlsx", ".xls"}

    def __init__(self, filepath: str, sheet_name: Optional[str] = None,
                 encoding: str = "utf-8", separator: str = ","):
        self.filepath = Path(filepath)
        self.sheet_name = sheet_name
        self.encoding = encoding
        self.separator = separator

    def load(self) -> pd.DataFrame:
        suffix = self.filepath.suffix.lower()

        if suffix not in self.SUPPORTED:
            raise ValueError(f"Formato não suportado: {suffix}. Use: {self.SUPPORTED}")

        if not self.filepath.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.filepath}")

        print(f"📂 Carregando: {self.filepath.name}")

        if suffix in (".csv", ".tsv"):
            sep = "\t" if suffix == ".tsv" else self.separator
            df = pd.read_csv(self.filepath, encoding=self.encoding, sep=sep)
        else:
            df = pd.read_excel(self.filepath, sheet_name=self.sheet_name or 0)

        # Remove colunas e linhas completamente vazias
        df = df.dropna(how="all", axis=0).dropna(how="all", axis=1)

        # Padroniza nomes de colunas: minúsculas, sem espaços
        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(r"[\s\-/]", "_", regex=True)
        )

        print(f"✅ {len(df)} linhas | {len(df.columns)} colunas carregadas")
        return df


# ── Exemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    loader = CSVLoader("data/raw/vendas_2024.csv")
    df = loader.load()
    print(df.dtypes)
