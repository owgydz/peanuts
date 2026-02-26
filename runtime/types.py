class PeanutType:
    def __repr__(self):
        return f"<PeanutType {self.__class__.__name__}>"


class PeanutNumber(int, PeanutType):
    pass


class PeanutString(str, PeanutType):
    pass


class PeanutBool(bool, PeanutType):
    pass