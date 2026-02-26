from parser.ast_nodes import *
from .formatter import Formatter
from .emitter import Emitter
from .errors import TranspileError


class Transpiler:
    def __init__(self):
        self.formatter = Formatter()
        self.emitter = Emitter()

    def transpile(self, program: Program):
        for statement in program.statements:
            self.emit_statement(statement)
        return self.formatter.output()

    def emit_statement(self, node):
        if isinstance(node, FunctionDef):
            self.emit_function(node)

        elif isinstance(node, VariableAssign):
            self.emit_variable(node)

        elif isinstance(node, IfStatement):
            self.emit_if(node)

        elif isinstance(node, ForLoop):
            self.emit_for(node)

        elif isinstance(node, ReturnStatement):
            self.emit_return(node)

        elif isinstance(node, Expression):
            # UNWRAP expression node properly
            value = self.emitter.emit_expression(node.value)
            self.formatter.write_line(value)

        elif isinstance(node, ImportStatement):
            self.emit_import(node)

        else:
            raise TranspileError(f"Unsupported statement {type(node)}")


    def emit_function(self, node: FunctionDef):
        params = ", ".join(node.params)
        self.formatter.write_line(f"def {node.name}({params}):")
        self.formatter.indent()
        self.emit_block(node.body)
        self.formatter.dedent()

    def emit_variable(self, node: VariableAssign):
        value = self.emitter.emit_expression(node.value)
        self.formatter.write_line(f"{node.name} = {value}")

    def emit_if(self, node: IfStatement):
        condition = self.emitter.emit_expression(node.condition)
        self.formatter.write_line(f"if {condition}:")
        self.formatter.indent()
        self.emit_block(node.body)
        self.formatter.dedent()

        if node.else_body:
            self.formatter.write_line("else:")
            self.formatter.indent()
            self.emit_block(node.else_body)
            self.formatter.dedent()

    def emit_for(self, node: ForLoop):
        iterable = self.emitter.emit_expression(node.iterable)
        self.formatter.write_line(
            f"for {node.iterator} in {iterable}:"
        )
        self.formatter.indent()
        self.emit_block(node.body)
        self.formatter.dedent()

    def emit_return(self, node: ReturnStatement):
        value = self.emitter.emit_expression(node.value)
        self.formatter.write_line(f"return {value}")

    def emit_block(self, block: Block):
        for stmt in block.statements:
            self.emit_statement(stmt)

    def emit_import(self, node: ImportStatement):
        self.formatter.write_line(
            f"{node.module_name} = __peanut_import('{node.module_name}')"
        )