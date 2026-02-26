class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}

    def define(self, name):
        self.symbols[name] = True

    def exists(self, name):
        if name in self.symbols:
            return True
        if self.parent:
            return self.parent.exists(name)
        return False