class LexerError(Exception):
    def __init__(self, message, line):
        super().__init__(f"[Line {line}] {message}")
        self.line = line