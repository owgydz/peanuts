class ParserError(Exception):
    def __init__(self, message, token=None):
        if token:
            message = f"[Line {token.line}] {message}"
        super().__init__(message)
        self.token = token