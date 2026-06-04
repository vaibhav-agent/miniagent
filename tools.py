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


def safe_eval(expression: str):
    expression = expression.replace(",", "")

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

            return SUPPORTED_OPERATORS[op_type](
                evaluate(node.operand)
            )

        raise ValueError("Invalid expression")

    return evaluate(tree)


def calculator(expression: str) -> str:
    try:
        result = safe_eval(expression)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return str(result)

    except Exception as e:
        return f"Error: {e}"