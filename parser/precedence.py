PRECEDENCE = {
    "OR": 1,
    "AND": 2,
    "EQUAL_EQUAL": 3,
    "BANG_EQUAL": 3,
    "GREATER": 4,
    "LESS": 4,
    "PLUS": 5,
    "MINUS": 5,
    "STAR": 6,
    "SLASH": 6,
}

def get_precedence(token_type):
    return PRECEDENCE.get(token_type.name, 0)