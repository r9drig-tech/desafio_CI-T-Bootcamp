"""
db_connector.py
Conexão e operações com bancos de dados (PostgreSQL).
Bootcamp CI&T — Do Prompt ao Agente
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text


class DBConnector:
    """Gerencia conexão com PostgreSQL via SQLAlchemy."""

    def __init__(self, host: str = None, port: int = 5432,
                 database: str = None, user: str = None, password: str = None):
        self.host     = host     or os.getenv("DB_HOST", "localhost")
        self.port     = port     or int(os.getenv("DB_PORT", 5432))
        self.database = database or os.getenv("DB_NAME", "data_warehouse")
        self.user     = user     or os.getenv("DB_USER", "postgres")
        self.password = password or os.getenv("DB_PASSWORD", "")
        self.engine   = None

    def connect(self) -> "DBConnector":
        url = (
            f"postgresql+psycopg2://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )
        self.engine = create_engine(url, pool_pre_ping=True)
        print(f"✅ Conectado em {self.host}/{self.database}")
        return self

    def query(self, sql: str, params: dict = None) -> pd.DataFrame:
        """Executa uma query SQL e retorna DataFrame."""
        if not self.engine:
            self.connect()
        with self.engine.connect() as conn:
            df = pd.read_sql(text(sql), conn, params=params)
        print(f"✅ {len(df)} registros retornados")
        return df

    def write(self, df: pd.DataFrame, table: str,
              schema: str = "public", if_exists: str = "append") -> None:
        """Salva um DataFrame em uma tabela do banco."""
        if not self.engine:
            self.connect()
        df.to_sql(table, self.engine, schema=schema,
                  if_exists=if_exists, index=False, chunksize=1000)
        print(f"✅ {len(df)} registros gravados em {schema}.{table}")

    def close(self) -> None:
        if self.engine:
            self.engine.dispose()
            print("🔌 Conexão encerrada")


# ── Exemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    db = DBConnector()
    df = db.query("SELECT * FROM fato_indicadores LIMIT 100")
    print(df.head())
    db.close()
