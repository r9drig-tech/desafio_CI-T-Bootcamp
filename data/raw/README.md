# 📂 Dados Brutos (Raw)

Pasta reservada para dados brutos extraídos das fontes originais.

## Fontes de dados
| Fonte | Descrição |
|-------|-----------|
| API BACEN | Indicadores econômicos do Banco Central do Brasil |
| CSV/Excel | Arquivos locais carregados via `csv_loader.py` |
| PostgreSQL | Dados extraídos via `db_connector.py` |

> ⚠️ Dados brutos não são versionados no Git.
> Execute `python src/main.py --pipeline ingestion` para gerar.
