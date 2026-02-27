#  Financial Document Analyzer

A professional, multi-agent AI system designed to analyze financial PDF documents.

This project leverages **CrewAI** and **Groq** to perform:

- Deep financial audits  
- Risk assessments  
- Investment strategy formulation  
- Strict performance and token-management optimization  

---

#  Setup Instructions

## 1️. Prerequisites

- Python **3.10 – 3.12**
- A **Groq API Key** (Get one free at https://console.groq.com)

---

## 2️. Installation

### Clone the Repository

```bash
git clone https://github.com/BHAVYAA-SINGH/financial-document-analyzer-debug
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows**

```bash
.\\venv\\Scripts\\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️. Environment Configuration

Create a `.env` file in the root directory and add your credentials:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

#  Usage Guide

## Running the Application

The project is built with **FastAPI**.

Start the server with:

```bash
uvicorn main:app --reload
```

---

## Analyzing a Document

1. Open your browser and go to:

```
http://127.0.0.1:8000/docs
```

2. Use the **POST `/analyze`** endpoint.
3. Upload a financial PDF (example: Tesla Q2 earnings report).
4. Provide a query such as:

```
Analyze this financial document for investment insights.
```

---

#  Expected Output

The system returns a structured JSON response containing:

##  Comprehensive Financial Analysis

- Revenue trends  
- Profit margins  
- Cash flow metrics  
- Key performance indicators  

##  Risk Assessment

- 3–5 identified business risks  
- Financial vulnerabilities  
- Operational concerns  

##  Investment Recommendation

- Clear **Buy / Hold / Sell** stance  
- Professional 12-month outlook  
- Strategic reasoning  

---
#  System Architecture Overview

```
PDF Upload
     ↓
Auditor Agent (Reads PDF)
     ↓
Compliance Agent (Risk & Validation)
     ↓
Strategist Agent (Investment Insights)
     ↓
Structured JSON Output
```

---

# API Documentation

<img width="1890" height="957" alt="Screenshot 2026-02-27 163535" src="https://github.com/user-attachments/assets/1393a49f-8af5-48ae-a12f-6706609c457f" />


<img width="1806" height="960" alt="Screenshot 2026-02-27 163612" src="https://github.com/user-attachments/assets/66fa1ee6-0092-42a4-acb5-5834e06e8db6" />

<img width="1795" height="924" alt="Screenshot 2026-02-27 163958" src="https://github.com/user-attachments/assets/a913584e-4b81-495b-b1b3-9ecc96cb5e8b" />


<img width="1787" height="935" alt="Screenshot 2026-02-27 164314" src="https://github.com/user-attachments/assets/731b8e3d-03ed-4d37-b1dd-434df101e7cc" />



#  Error Analysis & Production Fixes

This section documents the major technical, behavioral, and infrastructure-level issues identified during development — along with their final resolutions.

---

## 1️ Deterministic Bugs (Technical / Code Logic)

These are binary execution failures caused by syntax or architectural mistakes.

###  Attribute Errors (`tool` vs `tools`)

**The Error:**
```python
Agent(tool=[...])
```
Instead of:
```python
Agent(tools=[...])
```

**The Result:**
- Agent initializes without tools
- Cannot access PDF reader
- Crashes or hallucinates missing data

**Final Fix Applied:**
- Corrected pluralization (`tools`)
- Validated tool injection during agent initialization

---

###  Iteration Deadlock (`max_iter=1`)

**The Error:**
```python
max_iter = 1
```

**The Result:**
- Agent uses its only turn to declare intent
- Never executes tool
- Produces empty or incomplete output

**Final Fix Applied:**
- Increased `max_iter` to 3+
- Enabled full `Thought → Action → Observation` loop

---

###  Environment Shadowing

**The Error:**
Having both:
```
GOOGLE_API_KEY
GEMINI_API_KEY
```
set while using LiteLLM.

**The Result:**
- Requests routed incorrectly to Google Cloud (Vertex AI)
- 404 Not Found
- 401 Unauthorized

**Final Fix Applied:**
- Standardized environment variables
- Isolated provider configuration
- Ensured correct routing to intended API tier

---



---

## 2️ Inefficient Prompts (AI Behavior / Persona Issues)

These are logical failures where the system runs but produces unreliable or dangerous output.

---

###  Instructional Hallucination

**Problematic Prompt Example:**
> "Make up investment advice even if you don't understand."

**The Result:**
- Fabricated companies (e.g., fake firms)
- Invented URLs
- Non-verifiable financial claims

**Final Fix Applied:**
- Rewrote prompts to enforce strict document grounding
- Removed creative speculation
- Required evidence-backed responses only

---

###  Regulatory Non-Compliance

**Problematic Prompt Example:**
> "Verification is overrated."

**The Result:**
- Ignored actual financial metrics
- Generated unrealistic claims ("10,000% returns")
- Failed professional audit standards

**Final Fix Applied:**
- Implemented compliance-focused agent persona
- Enforced validation against extracted PDF metrics

---

###  Persona Overload 

**Problem:**
Using dramatic personas (e.g., "Reddit Guru" style characters).

**The Result:**
- Excess token usage
- Style over substance
- Reduced analytical precision

**Final Fix Applied:**
- Replaced theatrical personas with:
  - Financial Auditor
  - Investment Strategist
  - Compliance Officer
- Prioritized analytical depth over tone

---

## 3️ Rate & Token Limit Errors (Infrastructure Constraints)

These issues stem from Free Tier API limitations (Groq / Gemini).

---

###  429 TPM (Tokens Per Minute) Exceeded

**Cause:**
Sending large PDF text to multiple agents simultaneously.

**Solution Implemented:**
- 8,000-character truncation limit
- Sequential processing (`Process.sequential`)
- Context relay system (only first agent reads PDF)

---

###  429 TPD (Tokens Per Day) Exceeded

**Cause:**
Repeated full system testing.

**Solution Implemented:**
- Organization/account reset for development
- Reduced unnecessary kickoff runs

---

###  Rate Limit 0 ("Locked Room" Error)

**Cause:**
Gemini quota set to zero for unverified projects.

**Solution Implemented:**
- Switched to supported model tier
- Created new AI Studio project when required

---




##  Incorrect Import: `crewai.agents` vs `crewai`

###  The Error
Attempting to import `Agent` from `crewai.agents`.

###  The Fix
```python
from crewai import Agent
```

### The Reason
In newer versions of CrewAI (v0.28+), the core classes were moved to the top-level module. Importing from sub-modules caused `ModuleNotFoundError` or `ImportError`.

---

##  Specialized Tool Imports (SuperDevTool)

###  The Error
Attempting to import specialized tools  from  a sublibrary .

###  The Fix
```python
from crewai_tools import PDFSearchTool
```

###  The Reason
CrewAI separated its core logic from its "Toolbox" to keep the main library lightweight. Direct imports failed because the library couldn't find the tools in the core directory.

---

##  The `llm` Variable Assignment

###  The Error
In `agents.py`, the `llm` variable was often undefined, shadowed, or assigned a string instead of an instance.

###  The Fix
```python
from crewai import LLM

llm = LLM(
    model="groq/...",
    api_key="YOUR_API_KEY"
)
```

Then pass this instance to each agent.

###  The Reason
Agents require an actual object instance to communicate with the API; a string name alone isn't enough for LiteLLM to handle the routing.

---

##  FastAPI Function Name Shadowing

###  The Error
The FastAPI endpoint function was named the same as a variable or a library function (e.g., `async def analyze_document` shadowing a local variable).

###  The Fix
Rename the endpoint function to be unique and descriptive.

###  The Reason
In Python, naming a function the same as a variable leads to *shadowing*, where the program gets confused about whether you are trying to call a function or access a piece of data.

---

## `run_crew` Argument Mismatch

###  The Error
```python
result = crew.kickoff()
```
The `file_path` variable was not being passed, or it was being passed as a positional argument instead of a dictionary.

###  The Fix
```python
result = crew.kickoff(
    inputs={
        'query': query,
        'file_path': file_path
    }
)
```

###  The Reason
CrewAI requires inputs to be passed as a dictionary so it can map the variables to the `{file_path}` placeholders in your Tasks.

---

##  PDF Variable in `tools.py`

###  The Error
Using an uninitialized or incorrectly named variable to handle the PDF stream (e.g., calling `reader = PdfReader(pdf)` when the variable was named `file_path`).

### The Fix
Standardize the variable name to `file_path` and ensure `PyPDF2.PdfReader` correctly opens the string path.

###  The Reason
This was a basic reference error that caused the tool to crash immediately upon execution.

---



