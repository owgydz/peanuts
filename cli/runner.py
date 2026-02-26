from lexer.lexer import Lexer
from parser.parser import Parser
from transpile.transpiler import Transpiler
from runtime.environment import RuntimeEnvironment


def run_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    transpiler = Transpiler()
    python_code = transpiler.transpile(ast)
    with open("generated.py", "w") as f:
        f.write(python_code)
    runtime = RuntimeEnvironment()
    runtime.execute(python_code, filepath)


def build_file(filepath, output_path="build.py"):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    transpiler = Transpiler()
    python_code = transpiler.transpile(ast)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(python_code)

    print(f"Built → {output_path}")


def transpile_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    transpiler = Transpiler()
    python_code = transpiler.transpile(ast)

    print(python_code)