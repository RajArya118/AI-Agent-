import ast
import math
import operator

# Supported operators mapping
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Supported mathematical functions and constants
SAFE_MATH_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,
    "exp": math.exp,
    "ceil": math.ceil,
    "floor": math.floor,
    "radians": math.radians,
    "degrees": math.degrees,
    "factorial": math.factorial,
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "pow": pow,
}

SAFE_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}

def _eval_node(node):
    if isinstance(node, ast.Constant):  # Python 3.8+ (covers numbers)
        if isinstance(node.value, (int, float, complex)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        # Prevent huge exponents from exhausting CPU/memory
        if op_type == ast.Pow:
            if abs(right) > 1000:
                raise ValueError("Exponent too large (max: 1000)")
        return SAFE_OPERATORS[op_type](left, right)

    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _eval_node(node.operand)
        return SAFE_OPERATORS[op_type](operand)

    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only standard function names are permitted")
        func_name = node.func.id
        if func_name not in SAFE_MATH_FUNCTIONS:
            raise ValueError(f"Function '{func_name}' is not allowed or supported")
        args = [_eval_node(arg) for arg in node.args]
        return SAFE_MATH_FUNCTIONS[func_name](*args)

    elif isinstance(node, ast.Name):
        if node.id in SAFE_CONSTANTS:
            return SAFE_CONSTANTS[node.id]
        raise ValueError(f"Undefined variable or constant: '{node.id}'")

    else:
        raise ValueError(f"Unsupported syntax expression: {type(node).__name__}")

def safe_calculate(expression: str) -> dict:
    """
    Safely evaluate a mathematical expression using an AST parser.
    Blocks arbitrary code execution, imports, and variables.
    """
    try:
        cleaned = expression.strip()
        if not cleaned:
            return {"status": "error", "error": "Empty expression"}

        # Replace common mathematical symbols
        cleaned = cleaned.replace("×", "*").replace("÷", "/").replace("^", "**")
        
        tree = ast.parse(cleaned, mode="eval")
        result = _eval_node(tree.body)

        # Nicely format integer vs float results
        if isinstance(result, float) and result.is_integer():
            formatted = int(result)
        elif isinstance(result, float):
            formatted = round(result, 8)
        else:
            formatted = result

        return {
            "status": "success",
            "expression": expression,
            "result": formatted
        }
    except ZeroDivisionError:
        return {"status": "error", "error": "Division by zero is undefined."}
    except Exception as e:
        return {"status": "error", "error": f"Evaluation error: {str(e)}"}
