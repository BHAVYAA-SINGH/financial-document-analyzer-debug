## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier,risk_assessor, investment_advisor    
from tools import search_tool, FinancialDocumentTool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description=" Use the read_financial_document tool to extract data from {file_path}. Extract revenue trends, profit margins, and cash positions.\n",

    expected_output="A concise summary of key financial metrics and production data.",

    agent=financial_analyst,
    tools=[FinancialDocumentTool()],
    async_execution=False,
)




risk_assessment = Task(
    description="Based on the financial summary, identify 3-5 potential risks to the company's future growth.",
    expected_output="A detailed risk assessment report.",
    agent=risk_assessor,
    context=[analyze_financial_document],
    async_execution=False,
)



    
verification = Task(
    description="Cross-check the financial metrics extracted by the Analyst. Ensure the math adds up and there are no hallucinations.",

    expected_output="A brief confirmation or a list of corrected figures if any inconsistencies were found.",

    agent=risk_assessor,
    context=[analyze_financial_document],
    async_execution=False,
)

investment_analysis = Task(
    description="Synthesize the analysis and risk reports. Provide market insights and a Buy/Hold/Sell recommendation.",
    expected_output="A comprehensive final investment briefing.",

    agent=investment_advisor,
    context=[analyze_financial_document,risk_assessment,verification],
    async_execution=False,
)