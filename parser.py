from acyctokens import Ident, Num, Op, Char, String, Keyword, EOF
from acycast import *
from acycexceptions import *
import logging
from logging import debug, info

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
DEBUG_PARSE = False

priority_map = {"==": 10, "<=": 10, ">=": 10, "-": 50, "+": 50,
                "*": 60, "/": 60, "//": 60}


n = 0
def debug_calls(f):
    def g(*args, **kwargs):
        global n
        debug("  " * n + "enter " + f.__name__)
        n += 1
        x = f(*args, **kwargs)
        n -= 1
        debug("  " * n + "leave " + f.__name__)
        return x
    return g if DEBUG_PARSE else f

# ROOT := defn*
@debug_calls
def parse(tokens):
    definitions = []
    while not tokens.peek().isa(EOF):
        defn = parse_definition(tokens)
        definitions.append(defn)
    return definitions

# defn := <name> (defvar | deffn)
@debug_calls
def parse_definition(tokens):
    if tokens.peek().isa(Keyword):
        print(tokens.peek(), "is a keyword")
        return parse_data_definition(tokens)
    expect(tokens.peek(), Ident)
    name = tokens.peek().val
    tokens.advance()
    # If it's immediately followed by an '=', it's a variable
    if tokens.peek() == '=':
        tokens.advance()
        expr = parse_expression(tokens)
        return expr

    # If not immediately followed by an '=', then the function
    # pattern comes next
    pattern = parse_pattern(tokens)
    expect(tokens.peek(), '=')
    tokens.advance()
    expr = parse_expression(tokens)
    return FnAST(name, pattern, expr)


@debug_calls
def parse_primary_expression(tokens):
    token = tokens.peek()

    if token.isa(Num):
        tokens.advance()
        return NumAST(token.val)
    elif token.isa(Ident):
        name = token.val
        tokens.advance()
        if ((tokens.peek().isa(Ident) or tokens.peek() == '(' or
            tokens.peek().isa(Num)) and not tokens.on_new_line()):
            arg = parse_primary_expression(tokens)
            return FnCallAST(name, arg)
        return NameAST(name)
    elif token == '(':
        tokens.consume('(')
        exprs = [parse_expression(tokens)]
        while tokens.peek() == ',':
            tokens.consume(',')
            exprs.append(parse_expression(tokens))
        tokens.consume(')')
        if len(exprs) > 1:
            return TupleAST(exprs)
        else:
            return exprs[0]
    return None

# expr := letexpr | matchexpr | ifexpr | opexpr
@debug_calls
def parse_expression(tokens):
    token = tokens.peek()
    if token == "if":
        return parse_if(tokens)
    elif token == "match":
        return parse_match(tokens)
    elif token == "let":
        return parse_let(tokens)
    elif token.isa(Ident) or token.isa(Num):
        lhs = parse_primary_expression(tokens)
        return parse_expression_rhs(tokens, lhs, 0)
    elif token == '(':
        tokens.consume('(')
        expr = parse_expression(tokens)
        if tokens.next == ')':
            tokens.consume(')')
            return expr

        tuple_items = [expr]
        while tokens.peek() == ',':
            tokens.consume(',')
            tuple_items.append(parse_expression(tokens))
        tokens.consume(')')
        return TupleAST(tuple_items)
    return None

# letexpr := 'let' defn ( ';' defn )+ 'in' expr
@debug_calls
def parse_let(tokens):
    tokens.consume('let')
    defns = [parse_definition(tokens)]
    while tokens.peek() == ";":
        tokens.advance()
        defns.append(parse_definition(tokens))

    tokens.consume('in')
    body = parse_expression(tokens)
    return LetAST(defns, body)


# matchexpr := 'match' pattern 'for' ('case' pattern ('if' expr)? '=' expr)*
@debug_calls
def parse_match(tokens):
    tokens.consume("match")
    expr = parse_expression(tokens)
    tokens.consume("for")
    cases = []

    while tokens.peek() == "case":
        tokens.consume('case')

        if tokens.peek() == "if":
            tokens.advance()
            cond = parse_expression(tokens)
            pattern = CondPatternAST(cond)
        else:
            pattern = parse_pattern(tokens)

        tokens.consume("=")
        body = parse_expression(tokens)
        cases.append(CaseAST(pattern, body))

    return MatchAST(expr, cases)


# ifexpr := 'if' expr 'then' expr 'else' expr
@debug_calls
def parse_if(tokens):
    # cond, true, false = tokens.take('if', expr, 'then', expr, 'else', expr)

    tokens.consume("if")
    cond = parse_expression(tokens)
    tokens.consume("then")
    true = parse_expression(tokens)
    tokens.consume("else")
    false = parse_expression(tokens)

    return IfElseAST(cond, true, false)


@debug_calls
def parse_expression_rhs(tokens, lhs, prior):
    if not tokens.peek().isa(Op):
        return lhs

    lookahead = tokens.peek()
    while lookahead.isa(Op) and prior <= priority_map[lookahead.val]:
        op = lookahead.val
        tokens.advance()
        rhs = parse_primary_expression(tokens)
        lookahead = tokens.peek()
        while (lookahead.isa(Op) and
               priority_map[lookahead.val] > priority_map[op]):
            rhs = parse_expression_rhs(tokens, rhs,
                                       priority_map[lookahead.val])
            lookahead = tokens.peek()

        lhs = BinopAST(lhs, op, rhs)
    return lhs


# pattern := litpattern | '(' pattern ( ',' pattern )* ')' | upname '(' pattern ')'
@debug_calls
def parse_pattern(tokens):
    if tokens.peek() == '(':
        tokens.consume('(')
        if tokens.peek() == ')':
            tokens.consume(')')
            return UnitAST()
        subpattern = parse_pattern(tokens)
        if tokens.peek() == ')':
            tokens.consume(')')
            return subpattern

        subpatterns = [subpattern]
        while tokens.peek() == ',':
            tokens.consume(',')
            subpatterns.append(parse_pattern(tokens))
        tokens.consume(')')
        return TuplePatternAST(subpatterns)
    else:
        if tokens.peek().isa(Ident):
            name = tokens.peek().val
            if name[0].isupper():
                tokens.advance()
                tokens.consume('(')
                items = [parse_pattern(tokens)]
                while tokens.peek() == ',':
                    tokens.consume(',')
                    items.append(parse_pattern(tokens))
                
                return DataPatternAST(name, items)
            else:
                tokens.advance()
                return LitPatternAST(name)
        elif tokens.peek().isa(Num):
            val = tokens.peek().val
            tokens.advance()
            return LitPatternAST(val)
        else:
            unimplemented()


@debug_calls
def parse_data_definition(tokens):
    tokens.consume('data')
    expect(tokens.peek(), Ident)
    name = tokens.peek().val
    tokens.advance()
    
    if tokens.peek() == '(':
        tokens.consume('(')
        expect(tokens.peek(), Ident)
        params = [tokens.peek()]
        tokens.advance()
        while tokens.peek() == ',':
            tokens.consume(',')
            expect(tokens.peek(), Ident)
            params.append(tokens.peek())
        tokens.consume(')')
    tokens.consume('=')

    types = [parse_type(tokens)]
    while tokens.peek() == '|':
        tokens.consume('|')
        types.append(parse_type(tokens))

    return TypeAST(name, ConstructorAST(name, params), types)


@debug_calls
def parse_type(tokens):
    expect(tokens.peek(), Ident)
    typename = tokens.peek().val
    tokens.advance()
    params = []
    if tokens.peek() == '(':
        tokens.consume('(')
        params.append(parse_type(tokens))
        while tokens.peek() == ',':
            tokens.consume(',')
            params.append(parse_type(tokens))
        tokens.consume(')')

    return ConstructorAST(typename, params)

__all__ = (parse,)
