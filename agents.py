## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()


from crewai import Agent
from crewai import LLM


from tools import search_tool, FinancialDocumentTool

### Loading LLM
llm = LLM(model="groq/llama-3.3-70b-versatile")

# Creating an Experienced Financial Analyst agent
financial_analyst=Agent(
    role="Principal Financial Auditor",
    goal="Extract and verify raw financial data from the document for: {query}",
    verbose=True,
    memory=True,
    backstory=("You are a meticulous auditor. You provide the foundation of numbers for the rest of the team."),
    tools=[FinancialDocumentTool()],
    llm=llm,
    max_iter=3,
    max_rpm=2,
    allow_delegation=True  
)


risk_assessor = Agent(
    role="Risk Management Specialist",
    goal="Identify specific financial and operational risks based on the audit findings.",
    verbose=True,
    backstory=(
        "You look for red flags, volatility, and potential downsides in any investment."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=2,
    allow_delegation=False
)

verifier = Agent(
    role="Financial Verification Officer",
    goal="Verify that the Analyst's summary is logically consistent and matches the raw figures mentioned.",
    verbose=True,
    memory=True,
    backstory="You are a strict compliance officer. You do not read the PDF; you check the Analyst's work for errors.",
    llm=llm,
    max_iter=2,
    max_rpm=2,
    allow_delegation=False
)

investment_advisor = Agent(
    role="Chief Investment Officer",
    goal="Translate financial data into market insights and investment recommendations.",
    verbose=True,
    backstory=(
        "You are a high-level strategist who looks at the 'big picture' based on the numbers provided."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=2,
    allow_delegation=False
)



