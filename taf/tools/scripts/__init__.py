import click

from pathlib import Path

import ast

def extract_global_variables(filename):
    with open(filename, "r") as f:
        # Parse the Python file into an AST
        tree = ast.parse(f.read(), filename=filename)

    global_vars = {}

    # Walk through all nodes of the AST
    for node in ast.walk(tree):
        # We are interested in global variable assignments
        try:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        # We only extract simple variable assignments, not function definitions or imports
                        if isinstance(node.value, (ast.Constant, ast.List, ast.Dict, ast.Tuple, ast.Num, ast.Str)):
                            # Convert the AST expression to Python objects
                            global_vars[target.id] = ast.literal_eval(node.value)
        except:
            pass

    global_vars["__file__"] = filename

    return global_vars

def execute_command():
    @click.command(help="Executes an arbitrary python script")
    @click.argument("script_path")
    def execute(script_path):
        script_path = Path(script_path).resolve()
        global_scopes = extract_global_variables(script_path)
        # # globals_string = script_path.read_text()
        # globals_string = ((script_path.parent / "globals.py").read_text())
        # global_scope = {}
        # exec(globals_string, global_scope)
        with open(script_path, "r") as f:
            exec(f.read(), global_scopes)
    return execute


def attach_to_group(group):
    group.add_command(execute_command(), name='execute')