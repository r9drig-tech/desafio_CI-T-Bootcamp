"""
feature_eng.py
Feature Engineering para Machine Learning.
Bootcamp CI&T — Do Prompt ao Agente
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Optional
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler


class FeatureEngineer:
    """Prepara features para modelos de Machine Learning."""

    def __init__(self, df: pd.DataFrame):
        self._df = df.copy()
        self._encoders: dict  = {}
        self._scaler          = None

    # ── Encoding ─────────────────────────────────────────────────────────────

    def encode_categoricals(self, columns: Optional[List[str]] = None,
                            method: str = "label") -> "FeatureEngineer":
        """Codifica variáveis categóricas. method: 'label' | 'onehot'"""
        cols = columns or self._df.select_dtypes(include=["object", "category"]).columns.tolist()

        if method == "label":
            for col in cols:
                le = LabelEncoder()
                self._df[col] = le.fit_transform(self._df[col].astype(str))
                self._encoders[col] = le
            print(f"✅ Label Encoding aplicado em: {cols}")

        elif method == "onehot":
            self._df = pd.get_dummies(self._df, columns=cols, drop_first=True)
            print(f"✅ One-Hot Encoding aplicado em: {cols}")

        return self

    # ── Normalização ─────────────────────────────────────────────────────────

    def scale(self, columns: Optional[List[str]] = None,
              method: str = "standard") -> "FeatureEngineer":
        """Escala features numéricas. method: 'standard' | 'minmax'"""
        cols = columns or self._df.select_dtypes(include=[np.number]).columns.tolist()

        self._scaler = StandardScaler() if method == "standard" else MinMaxScaler()
        self._df[cols] = self._scaler.fit_transform(self._df[cols])
        print(f"✅ Scaling '{method}' aplicado em {len(cols)} colunas")
        return self

    # ── Features derivadas ───────────────────────────────────────────────────

    def add_lag_features(self, col: str, lags: List[int],
                         group_by: Optional[str] = None) -> "FeatureEngineer":
        """Cria features de lag (útil para séries temporais)."""
        for lag in lags:
            new_col = f"{col}_lag{lag}"
            if group_by:
                self._df[new_col] = self._df.groupby(group_by)[col].shift(lag)
            else:
                self._df[new_col] = self._df[col].shift(lag)
        print(f"✅ Lag features criadas: {[f'{col}_lag{l}' for l in lags]}")
        return self

    def add_rolling_features(self, col: str, windows: List[int],
                             group_by: Optional[str] = None) -> "FeatureEngineer":
        """Cria médias e desvios móveis."""
        for w in windows:
            if group_by:
                grp = self._df.groupby(group_by)[col]
                self._df[f"{col}_roll_mean_{w}"] = grp.transform(lambda x: x.rolling(w).mean())
                self._df[f"{col}_roll_std_{w}"]  = grp.transform(lambda x: x.rolling(w).std())
            else:
                self._df[f"{col}_roll_mean_{w}"] = self._df[col].rolling(w).mean()
                self._df[f"{col}_roll_std_{w}"]  = self._df[col].rolling(w).std()
        print(f"✅ Rolling features criadas para janelas: {windows}")
        return self

    def drop_nulls(self) -> "FeatureEngineer":
        before = len(self._df)
        self._df = self._df.dropna()
        print(f"✅ Removidas {before - len(self._df)} linhas com nulos após feature engineering")
        return self

    # ── Split ────────────────────────────────────────────────────────────────

    def split(self, target_col: str, test_size: float = 0.2,
              random_state: int = 42) -> Tuple:
        """Divide em treino e teste. Retorna X_train, X_test, y_train, y_test."""
        X = self._df.drop(columns=[target_col])
        y = self._df[target_col]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        print(f"✅ Split: treino={len(X_train)} | teste={len(X_test)}")
        return X_train, X_test, y_train, y_test

    def get_result(self) -> pd.DataFrame:
        return self._df


# ── Exemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = pd.DataFrame({
        "regiao": ["SP", "RJ", "MG", "SP", "RJ"] * 20,
        "valor":  np.random.randint(100, 1000, 100),
        "qtd":    np.random.randint(1, 50, 100),
        "target": np.random.randint(0, 2, 100),
    })

    fe = FeatureEngineer(df)
    X_train, X_test, y_train, y_test = (
        fe.encode_categoricals(["regiao"])
          .scale(["valor", "qtd"])
          .split(target_col="target")
    )
    print(f"X_train shape: {X_train.shape}")
