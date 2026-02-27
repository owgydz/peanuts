from .ast_nodes import *
from .errors import ParserError
from .precedence import get_precedence
from .scope import Scope


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_scope = Scope()


    def peek(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.tokens[self.position]
        self.position += 1
        return token

    def is_at_end(self):
        return self.peek().type.name == "EOF"

    def expect_type(self, type_name):
        token = self.peek()
        if token.type.name != type_name:
            raise ParserError(
                f"Expected {type_name}, got {token.type.name}",
                token
            )
        return self.advance()

    def match_type(self, type_name):
        if self.peek().type.name == type_name:
            return self.advance()
        return None

    def parse(self):
        statements = []

        while not self.is_at_end():
            if self.peek().type.name == "NEWLINE":
                self.advance()
                continue

            statements.append(self.parse_statement())

        return Program(statements)

    def parse_statement(self):
        token = self.peek()

        if token.type.name == "IMPORT":
            return self.parse_import()

        if token.type.name == "NUT":
            return self.parse_function()

        if token.type.name == "JAR":
            return self.parse_variable()

        if token.type.name == "CRUNCH":
            return self.parse_if()

        if token.type.name == "CHEW":
            return self.parse_for()

        if token.type.name == "SPREAD":
            return self.parse_return()

        return Expression(self.parse_expression())

    def parse_import(self):
        self.advance()
        module_name = self.expect_type("IDENTIFIER").value
        return ImportStatement(module_name)

    def parse_function(self):
        self.advance()
        name = self.expect_type("IDENTIFIER").value

        self.expect_type("LPAREN")
        params = self.parse_parameters()
        self.expect_type("RPAREN")
        self.expect_type("COLON")

        body = self.parse_block()

        return FunctionDef(name, params, body)

    def parse_variable(self):
        self.advance()
        name = self.expect_type("IDENTIFIER").value
        self.expect_type("EQUAL")
        value = self.parse_expression()
        return VariableAssign(name, value)

    def parse_if(self):
        self.advance()
        condition = self.parse_expression()
        self.expect_type("COLON")
        body = self.parse_block()

        else_body = None
        if self.peek().type.name == "OTHERWISE":
            self.advance()
            self.expect_type("COLON")
            else_body = self.parse_block()

        return IfStatement(condition, body, else_body)

    def parse_for(self):
        self.advance()
        iterator = self.expect_type("IDENTIFIER").value
        self.expect_type("IN")
        iterable = self.parse_expression()
        self.expect_type("COLON")
        body = self.parse_block()

        return ForLoop(iterator, iterable, body)

    def parse_return(self):
        self.advance()
        value = self.parse_expression()
        return ReturnStatement(value)

    def parse_block(self):
        self.expect_type("NEWLINE")
        self.expect_type("INDENT")

        statements = []

        while self.peek().type.name != "DEDENT":
            if self.peek().type.name == "NEWLINE":
                self.advance()
                continue
            statements.append(self.parse_statement())

        self.expect_type("DEDENT")
        return Block(statements)

    def parse_expression(self, precedence=0):
        left = self.parse_unary()

        while True:
            token = self.peek()
            token_precedence = get_precedence(token.type)

            if token_precedence <= precedence:
                break

            operator = self.advance()
            right = self.parse_expression(token_precedence)
            left = BinaryExpression(left, operator, right)

        return left

    def parse_unary(self):
        token = self.peek()

        if token.type.name in ("NOT", "MINUS"):
            operator = self.advance()
            operand = self.parse_unary()
            return UnaryExpression(operator, operand)

        return self.parse_primary()

    def parse_primary(self):
        token = self.advance()

        if token.type.name == "NUMBER":
            return Literal(token.value)

        if token.type.name == "STRING":
            return Literal(token.value)

        if token.type.name == "TRUE":
            return Literal(True)

        if token.type.name == "FALSE":
            return Literal(False)

        if token.type.name == "IDENTIFIER":
            node = Identifier(token.value)

            # Member access chain
            while self.peek().type.name == "DOT":
                self.advance()
                property_name = self.expect_type("IDENTIFIER").value
                node = MemberAccess(node, property_name)

            # Function call
            if self.peek().type.name == "LPAREN":
                return self.parse_call_from_node(node)

            return node

        raise ParserError("Unexpected token", token)

    def parse_call_from_node(self, node):
        self.expect_type("LPAREN")
        args = []

        if self.peek().type.name != "RPAREN":
            args.append(self.parse_expression())
            while self.match_type("COMMA"):
                args.append(self.parse_expression())

        self.expect_type("RPAREN")
        return CallExpression(node, args)

    def parse_parameters(self):
        params = []

        if self.peek().type.name != "RPAREN":
            params.append(self.expect_type("IDENTIFIER").value)
            while self.match_type("COMMA"):
                params.append(self.expect_type("IDENTIFIER").value)

        return params