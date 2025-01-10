import ast

def parse_code(code_input):
    """
    Parse and validate the input code
    """
    try:
        ast.parse(code_input)
        return code_input
    except SyntaxError as e:
        return f"# Invalid Python code\n{code_input}\n# Error: {str(e)}"