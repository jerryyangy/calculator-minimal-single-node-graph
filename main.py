
# minimal_calculator_graph.py
from typing import TypedDict
from langgraph.graph import StateGraph, END
import math

# ---- Safe evaluator: only math operators, no names allowed ----
def safe_eval(expr: str) -> float:
    # Compile and restrict names; allow operators and numeric literals
    code = compile(expr, "<expr>", "eval")
    if code.co_names:
        raise ValueError("Only numeric expressions are allowed (no variables/functions).")
    return eval(code, {"__builtins__": {}}, {})

# ---- Graph State ----
class CalcState(TypedDict):
    # user input
    input: str
    # result or error
    result: float | None
    error: str | None

# ---- Node ----
def evaluate_node(state: CalcState) -> CalcState:
    try:
        value = safe_eval(state["input"])
        return {**state, "result": float(value), "error": None}
    except Exception as e:
        return {**state, "result": None, "error": str(e)}

# ---- Build graph ----
builder = StateGraph(CalcState)
builder.add_node("evaluate", evaluate_node)
builder.set_entry_point("evaluate")
builder.add_edge("evaluate", END)
app = builder.compile()

if __name__ == "__main__":
    # Demo
    tests = [
        "12 * (3 + 5) / 2",
        "2 ** 10",
        "sqrt(9)",  # will error: names not allowed
        "10/0",     # will error: division by zero
    ]
    for t in tests:
        out = app.invoke({"input": t, "result": None, "error": None})
        print(f"Input: {t}\nOutput: {out}\n")
