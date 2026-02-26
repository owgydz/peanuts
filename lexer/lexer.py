from .token import Token
from .token_types import TokenType
from .errors import LexerError
from .indent import IndentHandler


KEYWORDS = {
    "nut": TokenType.NUT,
    "jar": TokenType.JAR,
    "crunch": TokenType.CRUNCH,
    "otherwise": TokenType.OTHERWISE,
    "chew": TokenType.CHEW,
    "spread": TokenType.SPREAD,
    "in": TokenType.IN,
    "import": TokenType.IMPORT,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
}


class Lexer:
    def __init__(self, source):
        self.source = source.splitlines()
        self.tokens = []
        self.line_number = 0
        self.indent_handler = IndentHandler()


    def tokenize(self):
        for raw_line in self.source:
            self.line_number += 1

            # Strip inline comments
            line = raw_line.split("#", 1)[0]

            if not line.strip():
                continue

            # Handle indentation
            self.tokens.extend(
                self.indent_handler.process(raw_line, self.line_number)
            )

            self.scan_line(line.strip())

            self.tokens.append(
                Token(TokenType.NEWLINE, line=self.line_number)
            )

        # Final dedents
        self.tokens.extend(
            self.indent_handler.finalize(self.line_number)
        )

        self.tokens.append(
            Token(TokenType.EOF, line=self.line_number)
        )

        return self.tokens


    def scan_line(self, line):
        i = 0

        while i < len(line):
            char = line[i]

            # Skip whitespace
            if char.isspace():
                i += 1
                continue

            if char.isalpha() or char == "_":
                start = i
                while i < len(line) and (
                    line[i].isalnum() or line[i] == "_"
                ):
                    i += 1

                text = line[start:i]
                token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)

                self.tokens.append(
                    Token(token_type, text, self.line_number)
                )
                continue

            if char.isdigit():
                start = i
                while i < len(line) and line[i].isdigit():
                    i += 1

                number = int(line[start:i])

                self.tokens.append(
                    Token(TokenType.NUMBER, number, self.line_number)
                )
                continue

            if char == '"':
                i += 1
                start = i

                while i < len(line) and line[i] != '"':
                    i += 1

                if i >= len(line):
                    raise LexerError(
                        "Unterminated string",
                        self.line_number
                    )

                value = line[start:i]
                i += 1

                self.tokens.append(
                    Token(TokenType.STRING, value, self.line_number)
                )
                continue

            # Two-character operators
            if char == ">" and i + 1 < len(line) and line[i + 1] == "=":
                self.tokens.append(
                    Token(TokenType.GREATER_EQUAL, ">=", self.line_number)
                )
                i += 2
                continue

            if char == "<" and i + 1 < len(line) and line[i + 1] == "=":
                self.tokens.append(
                    Token(TokenType.LESS_EQUAL, "<=", self.line_number)
                )
                i += 2
                continue

            if char == "=" and i + 1 < len(line) and line[i + 1] == "=":
                self.tokens.append(
                    Token(TokenType.EQUAL_EQUAL, "==", self.line_number)
                )
                i += 2
                continue

            if char == "!" and i + 1 < len(line) and line[i + 1] == "=":
                self.tokens.append(
                    Token(TokenType.BANG_EQUAL, "!=", self.line_number)
                )
                i += 2
                continue

            # Single-character operators
            if char == "+":
                self.tokens.append(Token(TokenType.PLUS, "+", self.line_number))
            elif char == "-":
                self.tokens.append(Token(TokenType.MINUS, "-", self.line_number))
            elif char == "*":
                self.tokens.append(Token(TokenType.STAR, "*", self.line_number))
            elif char == "/":
                self.tokens.append(Token(TokenType.SLASH, "/", self.line_number))
            elif char == "=":
                self.tokens.append(Token(TokenType.EQUAL, "=", self.line_number))
            elif char == ">":
                self.tokens.append(Token(TokenType.GREATER, ">", self.line_number))
            elif char == "<":
                self.tokens.append(Token(TokenType.LESS, "<", self.line_number))
            elif char == "(":
                self.tokens.append(Token(TokenType.LPAREN, "(", self.line_number))
            elif char == ")":
                self.tokens.append(Token(TokenType.RPAREN, ")", self.line_number))
            elif char == ":":
                self.tokens.append(Token(TokenType.COLON, ":", self.line_number))
            elif char == ",":
                self.tokens.append(Token(TokenType.COMMA, ",", self.line_number))
            elif char == ".":
                self.tokens.append(Token(TokenType.DOT, ".", self.line_number))
            else:
                raise LexerError(
                    f"Unexpected character '{char}'",
                    self.line_number
                )

            i += 1