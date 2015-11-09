from acyctokens import Num, Ident, Op, Char, String, Keyword, EOF
from acycexceptions import *


class TokenBuffer:
    def __init__(self, tokens):
        self.next = next(tokens)
        self.tokens = tokens
        self.previous_line = self.next.line

    def advance(self):
        try:
            self.previous_line = self.next.line
            self.next = next(self.tokens)
        except StopIteration:
            self.next = None

    def on_new_line(self):
        return (self.next.line != self.previous_line)

    def peek(self):
        return self.next

    def consume(self, item):
        expect(self.next, item)
        self.advance()


class StringBuffer:
    def __init__(self, string):
        self.string = string
        self.next = string[:1]
        self.index = 0
        self.line = 1
        self.col = 1

    def advance(self):
        if self.index is None:
            self.next = ""
            return

        if self.next == "\n":
            self.line += 1
            self.col = 1
        elif self.next != "":
            self.col += 1

        self.index += 1
        self.next = self.string[self.index:self.index+1]
        if self.next == "":
            self.index = None

    def peek(self):
        return self.next


def notempty(f):
    return lambda c: False if c is "" else f(c)


@notempty
def isident(c):
    c = ord(c)
    return (ord("A") <= c <= ord("Z") or
            ord("a") <= c <= ord("z") or
            ord("0") <= c <= ord("9") or
            c == ord("_"))


@notempty
def isop(c):
    return (c in "!$%&*+./<=>?@\^|-~:")


@notempty
def ispunct(c):
    return (c in "#()[]{},")


def tokenize(string):
    buf = StringBuffer(string)
    while True:
        if buf.peek() == "":
            break

        # Skip whitespace
        if buf.peek().isspace():
            buf.advance()
            continue
        # Capture identifiers
        # name := [_a-z][_A-Za-z0-9]
        elif buf.peek().isalpha():
            pos = buf.line, buf.col
            result = ""
            while isident(buf.peek()):
                result += buf.peek()
                buf.advance()

            keywords = {"if", "then", "else", "let", "in", "match", "for", "_",
                        "case", "data"}
            if result in keywords:
                yield Keyword(result, *pos)
            else:
                yield Ident(result, *pos)
        # Capture numbers
        # number := [0-9]+(.[0-9]*)?
        elif buf.peek().isdigit():
            pos = buf.line, buf.col
            result = ""
            while buf.peek().isdigit():
                result += buf.peek()
                buf.advance()
            if buf.peek() == ".":
                result += "."
                buf.advance()
                while buf.peek().isdigit():
                    result += buf.peek()
                    buf.advance()

            yield Num(float(result), *pos)
        # Capture operators
        elif isop(buf.peek()):
            pos = buf.line, buf.col
            result = ""
            while isop(buf.peek()):
                result += buf.peek()
                buf.advance()

            yield Keyword("=", *pos) if result == "=" else Op(result, *pos)
        # Skip comments
        elif buf.peek() == "#":
            while buf.peek() != "\n":
                buf.advance()
                # If we reach EOF
                if buf.peek() == "":
                    break
            continue
        # Capture punctuation
        elif ispunct(buf.peek()):
            yield Char(buf.peek(), buf.line, buf.col)
            buf.advance()
        # Capture strings
        elif buf.peek() == '"' or buf.peek() == "'":
            pos = buf.line, buf.col
            start = buf.peek()
            buf.advance()
            contents = ""
            while buf.peek() != start:
                if buf.peek() == "":
                    raise Exception("EOF in string")
                if buf.peek() == "\\":
                    buf.advance()  # Skip backslash
                    escapes = {"n": "\n", "\\": "\\", '"': '"', "'": "'"}
                    # Add the escaped character
                    contents += escapes[buf.peek()]
                    # Process the character after the escaped one
                    buf.advance()

                contents += buf.peek()
                buf.advance()

            buf.advance()
            yield String(contents, *pos)
        # Just advance normally
        else:
            buf.advance()

    yield EOF(None, buf.line, buf.col)

__all__ = (TokenBuffer, tokenize)
