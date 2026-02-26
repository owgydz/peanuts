import sys
import traceback
from datetime import datetime


PEANUT_PREFIX = "peanut_lang_output:"


class Colors:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"


class PeanutIO:
    def __init__(self):
        self.debug_mode = False
        self.use_prefix = True
        self.timestamp = False
        self.use_colors = True
        self.source_map = None  # used for stack trace mapping


    def enable_debug(self):
        self.debug_mode = True

    def enable_timestamp(self):
        self.timestamp = True

    def disable_colors(self):
        self.use_colors = False

    def set_source_map(self, source_map):
        self.source_map = source_map


    def colorize(self, text, color):
        if not self.use_colors:
            return text
        return f"{color}{text}{Colors.RESET}"

    def format_output(self, *args):
        parts = []

        if self.use_prefix:
            parts.append(self.colorize(PEANUT_PREFIX, Colors.YELLOW))

        if self.timestamp:
            parts.append(f"[{datetime.now().strftime('%H:%M:%S')}]")

        parts.extend(str(arg) for arg in args)
        return " ".join(parts)

    def write(self, *args):
        print(self.format_output(*args))

    def debug(self, *args):
        if self.debug_mode:
            print(self.format_output(
                self.colorize("[DEBUG]", Colors.CYAN),
                *args
            ))

    def error(self, *args):
        print(self.format_output(
            self.colorize("[ERROR]", Colors.RED),
            *args
        ), file=sys.stderr)


    def handle_exception(self, exc):
        if not self.source_map:
            raise exc

        tb = traceback.extract_tb(exc.__traceback__)
        mapped_lines = []

        for frame in tb:
            py_line = frame.lineno
            nut_line = self.source_map.get(py_line, None)

            if nut_line:
                mapped_lines.append(
                    f"  at {frame.name} (file.nut:{nut_line})"
                )
            else:
                mapped_lines.append(
                    f"  at {frame.name} (generated.py:{py_line})"
                )

        self.error("Runtime Error:", str(exc))
        print("\nStack trace:")
        for line in mapped_lines:
            print(line)


_peanut_io = PeanutIO()


def peanut_print(*args):
    _peanut_io.write(*args)


def peanut_debug(*args):
    _peanut_io.debug(*args)


def peanut_error(*args):
    _peanut_io.error(*args)


def peanut_input(prompt=""):
    return input(prompt)


def get_io():
    return _peanut_io