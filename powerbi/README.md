# 📊 Dashboard Power BI — Pipeline de Dados para IA

> **Bootcamp CI&T — Do Prompt ao Agente**

## Sobre o Dashboard

O arquivo `dashboard.pbix` contém o dashboard interativo conectado diretamente
ao Data Warehouse do pipeline.

## Páginas do Dashboard

| Página | Descrição |
|--------|-----------|
| 🏠 Overview | KPIs principais + resumo executivo gerado por IA |
| 📊 Análise Temporal | Tendências e sazonalidade dos indicadores |
| 🗺️ Mapa Regional | Distribuição geográfica dos dados |
| 🤖 Insights IA | Narrativas automáticas geradas por LLM |
| ⚙️ Pipeline Status | Monitoramento em tempo real do pipeline |

## Como conectar ao banco de dados

1. Abra o `dashboard.pbix` no Power BI Desktop
2. Vá em **Transformar Dados → Configurações da Fonte de Dados**
3. Atualize as credenciais do PostgreSQL:
   - Servidor: `localhost`
   - Banco: `data_warehouse`
   - Schema: `marts`
4. Clique em **Atualizar**

## Atualização automática

O dashboard está configurado para atualizar automaticamente
após cada execução do pipeline (a cada 30 minutos).

> ⚠️ O arquivo `.pbix` deve ser adicionado manualmente após
> criação no Power BI Desktop, pois arquivos binários não são
> gerados automaticamente por código.
