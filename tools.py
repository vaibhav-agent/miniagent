import ast
import operator

SUPPORTED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Guard against expressions that could hang or exhaust memory.
# e.g. 9**9**9 would run forever without this.
MAX_EXPRESSION_LENGTH = 200


def safe_eval(expression: str):
    expression = expression.replace(",", "").strip()

    if len(expression) > MAX_EXPRESSION_LENGTH:
        raise ValueError("Expression too long")

    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        elif isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float)):
                raise ValueError("Only numbers are allowed")
            return node.value

        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in SUPPORTED_OPERATORS:
                raise ValueError(f"Unsupported operator: {op_type}")
            left = evaluate(node.left)
            right = evaluate(node.right)
            return SUPPORTED_OPERATORS[op_type](left, right)

        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in SUPPORTED_OPERATORS:
                raise ValueError(f"Unsupported operator: {op_type}")
            return SUPPORTED_OPERATORS[op_type](evaluate(node.operand))

        raise ValueError("Invalid expression")

    return evaluate(tree)


def calculator(expression: str) -> str:
    """
    Evaluates a safe arithmetic expression and returns the result as a string.
    The model provides the expression; this function runs it.
    """
    try:
        result = safe_eval(expression)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def notes_lookup(query: str) -> dict:
    """
    Reads notes/college.md and returns both the raw content and the original
    query so the LLM in agent.py can extract the relevant answer.

    Returns a dict:
        {
            "query": <original query>,
            "content": <full file text>,
            "source": "notes/college.md"
        }

    On failure, "content" is an error string and "source" is None.
    """
    notes_path = "notes/college.md"
    try:
        with open(notes_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {
            "query": query,
            "content": content,
            "source": notes_path,
        }
    except FileNotFoundError:
        return {
            "query": query,
            "content": f"Error: '{notes_path}' not found. Create the file and try again.",
            "source": None,
        }
    except Exception as e:
        return {
            "query": query,
            "content": f"Error reading notes: {e}",
            "source": None,
        }