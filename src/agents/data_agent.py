"""
data_agent.py
Agente de análise autônoma de dados via LangChain + OpenAI.
Bootcamp CI&T — Do Prompt ao Agente
"""

import os
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# ── Ferramentas do agente ────────────────────────────────────────────────────

def build_data_tools(df: pd.DataFrame):
    """Cria ferramentas LangChain que operam sobre o DataFrame."""

    @tool
    def get_summary() -> str:
        """Retorna um resumo estatístico do dataset."""
        info = {
            "shape": df.shape,
            "colunas": df.columns.tolist(),
            "nulos": df.isnull().sum().to_dict(),
            "descricao": df.describe().to_dict(),
        }
        return str(info)

    @tool
    def run_query(query: str) -> str:
        """Executa uma query pandas no DataFrame. Ex: df[df['valor'] > 100].head()"""
        try:
            result = eval(query, {"df": df, "pd": pd})
            return str(result)
        except Exception as e:
            return f"Erro ao executar query: {e}"

    @tool
    def get_column_info(column: str) -> str:
        """Retorna informações detalhadas de uma coluna específica."""
        if column not in df.columns:
            return f"Coluna '{column}' não encontrada. Disponíveis: {df.columns.tolist()}"
        col = df[column]
        info = {
            "tipo": str(col.dtype),
            "nulos": int(col.isnull().sum()),
            "únicos": int(col.nunique()),
            "amostra": col.dropna().sample(min(5, len(col))).tolist(),
        }
        if pd.api.types.is_numeric_dtype(col):
            info.update({
                "min": float(col.min()),
                "max": float(col.max()),
                "média": float(col.mean()),
                "mediana": float(col.median()),
            })
        return str(info)

    return [get_summary, run_query, get_column_info]


# ── Agente principal ─────────────────────────────────────────────────────────

class DataAgent:
    """Agente autônomo de análise de dados usando LangChain."""

    SYSTEM_PROMPT = """Você é um Agente especialista em análise de dados.
Você tem acesso a um DataFrame pandas e pode usar as ferramentas disponíveis
para responder perguntas sobre os dados de forma precisa e objetiva.
Sempre baseie suas respostas nos dados reais retornados pelas ferramentas.
Responda sempre em português."""

    def __init__(self, df: pd.DataFrame, model: str = "gpt-4o", temperature: float = 0):
        self.df = df
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.tools = build_data_tools(df)
        self.agent = self._build_agent()

    def _build_agent(self) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_openai_functions_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def ask(self, question: str) -> str:
        """Faz uma pergunta ao agente sobre os dados."""
        print(f"\n🤖 Pergunta: {question}")
        result = self.agent.invoke({"input": question})
        answer = result.get("output", "Sem resposta")
        print(f"💡 Resposta: {answer}\n")
        return answer


# ── Exemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import numpy as np

    df = pd.DataFrame({
        "data":   pd.date_range("2024-01-01", periods=100, freq="D"),
        "regiao": np.random.choice(["SP", "RJ", "MG", "RS"], 100),
        "valor":  np.random.uniform(100, 5000, 100).round(2),
        "qtd":    np.random.randint(1, 50, 100),
    })

    agent = DataAgent(df)
    agent.ask("Qual região tem o maior valor médio de vendas?")
    agent.ask("Existem valores nulos no dataset? Em quais colunas?")
    agent.ask("Qual é a tendência de vendas ao longo do tempo?")
