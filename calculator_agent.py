import argparse
import os
import re

try:
    from langchain.agents import AgentType, Tool, initialize_agent
    from langchain.llms.groq import Groq
    LANGCHAIN_AVAILABLE = True
except ImportError:
    AgentType = Tool = initialize_agent = Groq = None
    LANGCHAIN_AVAILABLE = False

EXPRESSION_PATTERN = re.compile(r"^[0-9+\-*/().\s%^eE]+$")


def safe_calculator(expression: str) -> str:
    expression = expression.strip()
    if not expression:
        return "Error: expression is empty."
    if not EXPRESSION_PATTERN.fullmatch(expression):
        return "Error: expression contains invalid characters. Use only numbers, operators, and parentheses."

    try:
        allowed_names = {
            "abs": abs,
            "round": round,
            "pow": pow,
        }
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return str(result)
    except Exception as exc:
        return f"Error evaluating expression: {exc}"


def build_agent() -> object:
    if not LANGCHAIN_AVAILABLE:
        raise RuntimeError(
            "LangChain/Groq is not installed or not importable. "
            "Install requirements with: python -m pip install -r requirements.txt"
        )

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is required. Set it in your environment before running.")

    llm = Groq(api_key=api_key, model="groq-1.5-mini", temperature=0.0)

    calculator_tool = Tool(
        name="Calculator",
        func=safe_calculator,
        description=(
            "Use this tool to compute exact numeric expressions. "
            "Input should be a math expression using numbers, +, -, *, /, ^, %, parentheses, and functions like abs()."
        ),
    )

    return initialize_agent(
        tools=[calculator_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="LangChain calculator agent powered by Groq.")
    parser.add_argument("--query", type=str, help="Math question or expression to evaluate.")
    args = parser.parse_args()

    if LANGCHAIN_AVAILABLE:
        try:
            agent = build_agent()
        except RuntimeError as exc:
            print(f"Warning: {exc}")
            agent = None
    else:
        print("Warning: LangChain/Groq is not installed. Running local calculator fallback.")
        agent = None

    if args.query:
        if agent is not None:
            response = agent.run(args.query)
        else:
            response = safe_calculator(args.query)
        print(response)
        return

    print("Interactive calculator agent. Type a math question and press Enter. Ctrl+C to exit.")
    if agent is None:
        print("Local fallback mode: calculator expressions only.")

    while True:
        try:
            question = input("Question> ").strip()
            if not question:
                continue
            if agent is not None:
                print(agent.run(question))
            else:
                print(safe_calculator(question))
        except KeyboardInterrupt:
            print("\nExiting.")
            break


if __name__ == "__main__":
    main()
