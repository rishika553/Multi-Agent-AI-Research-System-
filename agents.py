from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv
load_dotenv()

#model setup
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)

#1st  agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

#2nd agent

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )

#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert research writer.write clear , structured and insightful summaries of the given text."),
        ("human", """Write a detailed research report o the topic below.
Topic: {topic}
Research Gathered:
{research}

Structure the report as :
1. Introduction 
2. key findings(minimum 3 well - explained points)
3. conclusion
4. sources (list all URLs found in the research)
Be detailed , factual and professional."""),
    ])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a critical reviewer of research reports. You will evaluate the given report for clarity, accuracy, and depth of analysis."),
    ("human", """Critically review the following research report.           

Report:
{report}
respond in the exact format:
score: X/10
strengths:
- ...
- ...

 Areas for improvement:
 - ...
 - ...

one line verdict: 
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()

