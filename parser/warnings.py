from .ast_nodes import *


def analyze_warnings(program):
    declared = {}
    used = set()

    def visit(node):
        if isinstance(node, VariableAssign):
            if node.name in declared:
                print(f"Warning: Variable '{node.name}' redefined")
            declared[node.name] = node

            visit(node.value)

        elif isinstance(node, Identifier):
            used.add(node.name)

        elif isinstance(node, FunctionDef):
            for stmt in node.body.statements:
                visit(stmt)

        elif isinstance(node, Block):
            for stmt in node.statements:
                visit(stmt)

        elif isinstance(node, IfStatement):
            visit(node.condition)
            visit(node.body)
            if node.else_body:
                visit(node.else_body)

        elif isinstance(node, ForLoop):
            visit(node.iterable)
            visit(node.body)

        elif isinstance(node, ReturnStatement):
            visit(node.value)

        elif isinstance(node, Expression):
            visit(node.value)

        elif isinstance(node, BinaryExpression):
            visit(node.left)
            visit(node.right)

        elif isinstance(node, CallExpression):
            visit(node.callee)
            for arg in node.arguments:
                visit(arg)

        elif isinstance(node, MemberAccess):
            visit(node.object)

        elif isinstance(node, Program):
            for stmt in node.statements:
                visit(stmt)

    visit(program)

    # Unused variable detection
    for name in declared:
        if name not in used:
            print(f"Warning: Variable '{name}' declared but never used")