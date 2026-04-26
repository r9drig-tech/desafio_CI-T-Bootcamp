"""
llm_integration.py
Integração com LLMs via OpenAI API — funções utilitárias reutilizáveis.
Bootcamp CI&T — Do Prompt ao Agente
"""

import os
import json
from typing import Optional, List, Dict
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DEFAULT_MODEL = "gpt-4o"


# ── Funções utilitárias ──────────────────────────────────────────────────────

def chat(prompt: str, system: str = "Você é um assistente útil. Responda em português.",
         model: str = DEFAULT_MODEL, temperature: float = 0.3,
         max_tokens: int = 1000) -> str:
    """
    Chamada simples de chat completion.

    Args:
        prompt:      Mensagem do usuário
        system:      Instrução de sistema
        model:       Modelo OpenAI
        temperature: Criatividade (0 = determinístico, 1 = criativo)
        max_tokens:  Limite de tokens na resposta

    Returns:
        Resposta do modelo como string
    """
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def chat_json(prompt: str, system: str = None,
              model: str = DEFAULT_MODEL) -> dict:
    """
    Chamada que força retorno em JSON.
    Útil para gerar dados estruturados.
    """
    system_prompt = system or (
        "Você é um assistente que retorna APENAS JSON válido, sem markdown, "
        "sem explicações. Responda sempre com um objeto JSON."
    )
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt},
        ],
    )
    raw = response.choices[0].message.content.strip()
    return json.loads(raw)


def multi_turn_chat(messages: List[Dict[str, str]],
                    model: str = DEFAULT_MODEL,
                    temperature: float = 0.3) -> str:
    """
    Chat com histórico de mensagens (multi-turn).

    Args:
        messages: Lista de dicts com 'role' e 'content'
                  Ex: [{"role": "user", "content": "Olá"}, ...]
    """
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
    )
    return response.choices[0].message.content.strip()


def summarize(text: str, max_words: int = 100,
              language: str = "português") -> str:
    """Resume um texto longo."""
    prompt = f"Resuma o texto abaixo em no máximo {max_words} palavras em {language}:\n\n{text}"
    return chat(prompt, temperature=0.2)


def classify(text: str, categories: List[str]) -> str:
    """Classifica um texto em uma das categorias fornecidas."""
    prompt = (
        f"Classifique o texto abaixo em UMA das categorias: {categories}.\n"
        f"Retorne APENAS o nome da categoria, sem explicação.\n\n"
        f"Texto: {text}"
    )
    return chat(prompt, temperature=0)


def extract_entities(text: str) -> dict:
    """Extrai entidades nomeadas de um texto (pessoas, datas, locais, valores)."""
    prompt = (
        f"Extraia entidades do texto abaixo e retorne um JSON com as chaves: "
        f"pessoas, organizacoes, locais, datas, valores_monetarios.\n\n"
        f"Texto: {text}"
    )
    return chat_json(prompt)


def explain_data(summary: str, audience: str = "executivos de negócio") -> str:
    """Transforma um resumo técnico em linguagem acessível para o público alvo."""
    system = (
        f"Você é um especialista em comunicação de dados. "
        f"Traduza insights técnicos para {audience} de forma clara e objetiva."
    )
    return chat(summary, system=system, temperature=0.4)


# ── Exemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Chat simples
    response = chat("Quais são os principais indicadores de qualidade de um pipeline de dados?")
    print("💬 Chat:\n", response)

    # JSON estruturado
    result = chat_json(
        "Liste 3 métricas KPI para uma área de vendas com nome, descrição e unidade."
    )
    print("\n📦 JSON:\n", json.dumps(result, ensure_ascii=False, indent=2))

    # Classificação
    categoria = classify(
        "As vendas caíram 20% no último trimestre devido à sazonalidade.",
        categories=["alerta", "positivo", "neutro", "oportunidade"]
    )
    print(f"\n🏷️ Categoria: {categoria}")

    # Extração de entidades
    entidades = extract_entities(
        "A CI&T contratou Rodrigo Salgado em São Paulo em janeiro de 2024 "
        "por R$ 12.000 mensais."
    )
    print("\n🔍 Entidades:\n", json.dumps(entidades, ensure_ascii=False, indent=2))
