# LangChain Calculator Agent (Groq)

A minimal Python example showing how to build a LangChain calculator agent backed by a Groq LLM.

## Setup

1. Create and activate a Python environment.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Set your Groq API key:

```powershell
$Env:GROQ_API_KEY = "your_groq_api_key"
```

## Run

Interactive mode:

```bash
python calculator_agent.py
```

One-shot query:

```bash
python calculator_agent.py --query "12 / 4 + 3"
```

## Notes

- The agent uses a safe calculator tool for numeric expressions.
- The LLM is used to interpret the intent and decide when to call the calculator.
