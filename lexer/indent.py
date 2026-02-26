from .token_types import TokenType
from .token import Token


class IndentHandler:
    def __init__(self):
        self.indent_stack = [0]

    def process(self, line, line_number):
        tokens = []
        stripped = line.lstrip("\t ")
        indent = len(line) - len(stripped)

        current = self.indent_stack[-1]

        if indent > current:
            self.indent_stack.append(indent)
            tokens.append(Token(TokenType.INDENT, line=line_number))

        while indent < current:
            self.indent_stack.pop()
            current = self.indent_stack[-1]
            tokens.append(Token(TokenType.DEDENT, line=line_number))

        return tokens

    def finalize(self, line_number):
        tokens = []
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            tokens.append(Token(TokenType.DEDENT, line=line_number))
        return tokens