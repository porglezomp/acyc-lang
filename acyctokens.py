class Token:
    def __init__(self, val, line, col):
        self.val, self.line, self.col = val, line, col

    def __repr__(self):
        return "{}({})".format(
            str(self.__class__).split("'")[1].split(".")[-1],
            repr(self.val)
        )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.val == other.val)
        else:
            return (self.val == other)

    def __ne__(self, other):
        return not (self == other)

    def isa(self, type_t):
        return isinstance(self, type_t)

class Ident (Token): pass
class Num (Token): pass
class Op (Token): pass
class Char (Token): pass
class String (Token): pass
class Keyword (Token): pass
class EOF (Token): pass
