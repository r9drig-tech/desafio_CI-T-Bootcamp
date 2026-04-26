"""
api_extractor.py
Extração de dados de APIs públicas (REST).
Bootcamp CI&T — Do Prompt ao Agente
"""

import requests
import pandas as pd
from typing import Optional


class APIExtractor:
    """Extrai dados de APIs públicas REST e retorna um DataFrame."""

    def __init__(self, base_url: str, endpoint: str, params: Optional[dict] = None):
        self.base_url = base_url.rstrip("/")
        self.endpoint = endpoint
        self.params = params or {}

    def extract(self) -> pd.DataFrame:
        url = f"{self.base_url}{self.endpoint}"
        print(f"🔗 Conectando em: {url}")

        response = requests.get(url, params=self.params, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Aceita lista de dicts ou dict com chave 'data'/'results'/'value'
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            for key in ("data", "results", "value", "items"):
                if key in data:
                    df = pd.DataFrame(data[key])
                    break
            else:
                df = pd.DataFrame([data])
        else:
            raise ValueError(f"Formato de resposta inesperado: {type(data)}")

        print(f"✅ {len(df)} registros extraídos de {url}")
        return df


# ── Exemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    # API pública do Banco Central do Brasil (BACEN)
    extractor = APIExtractor(
        base_url="https://api.bcb.gov.br/dados/serie",
        endpoint="/bcdata.sgs.1/dados",
        params={"formato": "json", "dataInicial": "01/01/2024"},
    )
    df = extractor.extract()
    print(df.head())
