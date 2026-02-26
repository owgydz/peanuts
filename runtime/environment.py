import os
import types
import traceback
import time

from .builtins import build_builtins
from .io import get_io

from lexer.lexer import Lexer
from parser.parser import Parser
from transpile.transpiler import Transpiler


class RuntimeEnvironment:
    def __init__(self, source_map=None):
        self.globals = {}
        self.modules = {}
        self.io = get_io()
        self.io.set_source_map(source_map)

        builtins = build_builtins()
        builtins["__peanut_import"] = self.import_module

        self.globals["__builtins__"] = builtins


    def import_module(self, module_name):
        if module_name in self.modules:
            return self.modules[module_name]

        module_path = self.find_module(module_name)

        if not module_path:
            raise Exception(f"Module '{module_name}' not found")

        with open(module_path, "r", encoding="utf-8") as f:
            source = f.read()

        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        transpiler = Transpiler()
        python_code = transpiler.transpile(ast)

        module_namespace = {}
        exec(python_code, self.globals, module_namespace)

        clean_namespace = {
            k: v for k, v in module_namespace.items()
            if not k.startswith("__")
        }

        module = types.SimpleNamespace(**clean_namespace)
        self.modules[module_name] = module

        return module

    def find_module(self, module_name):
        # Check stdlib
        stdlib_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "stdlib",
            f"{module_name}.nut"
        )

        if os.path.exists(stdlib_path):
            return stdlib_path

        # Check installed packages
        pkg_path = os.path.join(
            ".peanuts",
            "packages",
            module_name,
            f"{module_name}.nut"
        )

        if os.path.exists(pkg_path):
            return pkg_path

        return None


    def execute(self, python_code: str, filename="(runtime)"):
        start_time = time.time()

        try:
            exec(python_code, self.globals)

        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)

            if tb:
                last = tb[-1]
                line_number = last.lineno
                function_name = last.name
            else:
                line_number = "unknown"
                function_name = "unknown"

            print("\n🥜 Runtime Error")
            print(f"  File: {filename}")
            print(f"  Line: {line_number}")
            print(f"  In: {function_name}()")
            print(f"  Message: {str(e)}")

        finally:
            if self.io.debug_mode:
                duration = time.time() - start_time
                print(f"\n🥜 [DEBUG] Execution time: {duration:.6f}s")