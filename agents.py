import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url

load_dotenv()


# =========================
# CONFIGURATION
# =========================

def get_config(key):
    # Read from Streamlit Cloud Secrets first
    try:
        import streamlit as st
        value = st.secrets.get(key)

        if value:
            return value
    except Exception:
        pass

    # Fallback to local .env
    return os.getenv(key)


OPENROUTER_API_KEY = get_config("OPENROUTER_API_KEY")
OPENAI_MODEL = get_config("OPENAI_MODEL")

if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY is missing. "
        "Add it to Streamlit Cloud Secrets or your local .env file."
    )

if not OPENAI_MODEL:
    raise ValueError(
        "OPENAI_MODEL is missing. "
        "Add it to Streamlit Cloud Secrets or your local .env file."
    )


# =========================
# MODEL SETUP
# =========================

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)


# =========================
# SEARCH AGENT
# =========================

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )


# =========================
# READER AGENT
# =========================

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


# =========================
# WRITER CHAIN
# =========================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. "
        "Write clear, structured, and insightful research reports."
    ),
    (
        "human",
        """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:

1. Introduction
2. Key findings (minimum 3 well-explained points)
3. Conclusion
4. Sources (list all URLs found in the research)

Be detailed, factual, and professional."""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# =========================
# CRITIC CHAIN
# =========================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a critical reviewer of research reports. "
        "Evaluate the report for clarity, accuracy, and depth of analysis."
    ),
    (
        "human",
        """Critically review the following research report.

Report:
{report}

Respond in the exact format:

Score: X/10

Strengths:
- ...
- ...

Areas for improvement:
- ...
- ...

One-line verdict:
..."""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()