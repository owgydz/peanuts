class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class VariableAssign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class IfStatement(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body


class ForLoop(ASTNode):
    def __init__(self, iterator, iterable, body):
        self.iterator = iterator
        self.iterable = iterable
        self.body = body


class ReturnStatement(ASTNode):
    def __init__(self, value):
        self.value = value


class Expression(ASTNode):
    def __init__(self, value):
        self.value = value


class CallExpression(ASTNode):
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name


class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

class ImportStatement(ASTNode):
    def __init__(self, module_name):
        self.module_name = module_name

class MemberAccess(ASTNode):
    def __init__(self, object_, property_):
        self.object = object_
        self.property = property_