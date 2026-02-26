class PeanutsRuntimeError(Exception):
    def __init__(self, message):
        super().__init__(f"[Peanuts Runtime] {message}")