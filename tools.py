## Importing libraries and files
import os
import PyPDF2 as Pdf
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import tools
from crewai.tools import BaseTool

from crewai_tools import SerperDevTool
# I couldn't use pdfserarchtool because it has dependancy on openai library which is not compatible with groq's llm, so I created a custom pdf reader tool using PyPDF2 to extract text from the financial document. 
#from crewai_tools import PDFSearchTool

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool(BaseTool):
    name:str = "read_financial_document"
    description:str = "MANDATORY: Use this tool to retrieve the actual financial data from the uploaded PDF. You are FORBIDDEN from providing an analysis without the data from this tool."

    def _run(self, path: str='data/sample.pdf') -> str:
        full_report = ""

        with open(path, 'rb') as file:
            docs = Pdf.PdfReader(file)

            for data in docs.pages:
                content = data.extract_text()

                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                
                full_report += content + "\n"
            #I have to limit the report size because of the token limit of the model, but in a real use case, we would want to process the entire document
        return full_report[:8000]  

## Creating Investment Analysis Tool
class InvestmentTool:
    async def analyze_investment_tool(financial_document_data):
        # Process and analyze the financial document data
        processed_data = financial_document_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement investment analysis logic here
        return "Investment analysis functionality to be implemented"

## Creating Risk Assessment Tool
class RiskTool:
    async def create_risk_assessment_tool(financial_document_data):        
        # TODO: Implement risk assessment logic here
        return "Risk assessment functionality to be implemented"