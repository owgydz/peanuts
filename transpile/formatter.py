class Formatter:
    def __init__(self):
        self.indent_level = 0
        self.lines = []

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level -= 1

    def write_line(self, line=""):
        indentation = "    " * self.indent_level
        self.lines.append(f"{indentation}{line}")

    def output(self):
        return "\n".join(self.lines)