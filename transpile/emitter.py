from parser.ast_nodes import *


class Emitter:
    def emit_expression(self, node):
        if isinstance(node, Literal):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            return str(node.value)
        
        if isinstance(node, Identifier):
            return node.name
        
        if isinstance(node, MemberAccess):
            obj = self.emit_expression(node.object)
            return f"{obj}.{node.property}"
        
        if isinstance(node, BinaryExpression):
            left = self.emit_expression(node.left)
            right = self.emit_expression(node.right)
            return f"{left} {node.operator.value} {right}"
        
        if isinstance(node, CallExpression):
            callee = self.emit_expression(node.callee)
            args = ", ".join(
                self.emit_expression(arg)
                for arg in node.arguments
            )
            return f"{callee}({args})"

        raise Exception(f"Unsupported expression: {type(node)}")