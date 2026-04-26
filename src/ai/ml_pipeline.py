"""
ml_pipeline.py
Pipeline completo de Machine Learning com Scikit-learn.
Bootcamp CI&T — Do Prompt ao Agente
"""

import os
import pickle
from pathlib import Path
from typing import Tuple, Dict, Optional, Literal

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    r2_score, mean_absolute_error, mean_squared_error,
)
from sklearn.model_selection import cross_val_score


TaskType = Literal["classification", "regression"]
Algorithm = Literal["random_forest", "gradient_boosting", "logistic_regression", "linear_regression"]


class MLPipeline:
    """Pipeline de treino, avaliação e predição de modelos de ML."""

    MODELS = {
        "classification": {
            "random_forest":      RandomForestClassifier(n_estimators=100, random_state=42),
            "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
        },
        "regression": {
            "random_forest":       RandomForestRegressor(n_estimators=100, random_state=42),
            "gradient_boosting":   GradientBoostingRegressor(n_estimators=100, random_state=42),
            "linear_regression":   LinearRegression(),
        },
    }

    def __init__(self, task: TaskType = "regression"):
        self.task    = task
        self.model   = None
        self.feature_names: list = []

    # ── Treino ───────────────────────────────────────────────────────────────

    def train(self, X_train: pd.DataFrame, y_train: pd.Series,
              algorithm: Algorithm = "random_forest") -> "MLPipeline":
        """Treina o modelo escolhido."""
        available = self.MODELS.get(self.task, {})
        if algorithm not in available:
            raise ValueError(f"Algoritmo '{algorithm}' não disponível para '{self.task}'. "
                             f"Disponíveis: {list(available.keys())}")

        self.model = available[algorithm]
        self.feature_names = X_train.columns.tolist()

        print(f"🤖 Treinando {algorithm} ({self.task})...")
        self.model.fit(X_train, y_train)
        print("✅ Treino concluído!")
        return self

    # ── Avaliação ────────────────────────────────────────────────────────────

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """Avalia o modelo e retorna métricas."""
        if not self.model:
            raise RuntimeError("Modelo não treinado. Chame .train() primeiro.")

        y_pred = self.model.predict(X_test)

        if self.task == "classification":
            metrics = {
                "accuracy":  round(accuracy_score(y_test, y_pred), 4),
                "f1":        round(f1_score(y_test, y_pred, average="weighted"), 4),
                "precision": round(precision_score(y_test, y_pred, average="weighted"), 4),
                "recall":    round(recall_score(y_test, y_pred, average="weighted"), 4),
            }
        else:
            metrics = {
                "r2":   round(r2_score(y_test, y_pred), 4),
                "mae":  round(mean_absolute_error(y_test, y_pred), 4),
                "rmse": round(np.sqrt(mean_squared_error(y_test, y_pred)), 4),
            }

        print("\n📊 Métricas de Avaliação:")
        for k, v in metrics.items():
            print(f"  ▸ {k.upper()}: {v}")
        return metrics

    def cross_validate(self, X: pd.DataFrame, y: pd.Series, cv: int = 5) -> Dict[str, float]:
        """Avaliação com cross-validation."""
        if not self.model:
            raise RuntimeError("Modelo não treinado.")
        scoring = "accuracy" if self.task == "classification" else "r2"
        scores = cross_val_score(self.model, X, y, cv=cv, scoring=scoring)
        result = {"cv_mean": round(scores.mean(), 4), "cv_std": round(scores.std(), 4)}
        print(f"✅ Cross-Validation ({cv} folds): {result['cv_mean']} ± {result['cv_std']}")
        return result

    # ── Feature Importance ───────────────────────────────────────────────────

    def feature_importance(self, top_n: int = 10) -> pd.DataFrame:
        """Retorna as features mais importantes do modelo (tree-based)."""
        if not hasattr(self.model, "feature_importances_"):
            print("⚠️ Este modelo não suporta feature_importances_")
            return pd.DataFrame()

        fi = pd.DataFrame({
            "feature":    self.feature_names,
            "importance": self.model.feature_importances_,
        }).sort_values("importance", ascending=False).head(top_n)

        print(f"\n🔍 Top {top_n} Features Importantes:")
        print(fi.to_string(index=False))
        return fi

    # ── Predição ─────────────────────────────────────────────────────────────

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if not self.model:
            raise RuntimeError("Modelo não treinado.")
        return self.model.predict(X)

    # ── Persistência ─────────────────────────────────────────────────────────

    def save(self, path: str = "models/model.pkl") -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self.model, f)
        print(f"✅ Modelo salvo em: {path}")

    def load(self, path: str = "models/model.pkl") -> "MLPipeline":
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        print(f"✅ Modelo carregado de: {path}")
        return self


# ── Exemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    from sklearn.datasets import make_regression
    from sklearn.model_selection import train_test_split

    X, y = make_regression(n_samples=500, n_features=10, noise=0.1, random_state=42)
    X = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])
    y = pd.Series(y, name="target")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = MLPipeline(task="regression")
    pipeline.train(X_train, y_train, algorithm="random_forest")
    metrics = pipeline.evaluate(X_test, y_test)
    pipeline.feature_importance()
    pipeline.save("models/regression_model.pkl")
