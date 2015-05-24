from collections import namedtuple


BinopAST = namedtuple('BinopAST', 'lhs, op, rhs')
FnAST = namedtuple('FnAST', 'args, body')
FnCallAST = namedtuple('FnCallAST', 'name, args')
AssignmentAST = namedtuple('AssignmentAST', 'name, val')
IfElseExprAST = namedtuple('IfElseExprAST', 'cond, true, false')
MatchAST = namedtuple('MatchAST', 'expr, cases')
CaseAST = namedtuple('CaseAST', 'pattern, body')
LetAST = namedtuple('LetAST', 'defns, body')

PatternAST = namedtuple('PatternAST', 'pattern')
TuplePatternAST = namedtuple('TuplePatternAST', 'patterns')
CondPatternAST = namedtuple('CondPatternAST', 'cond')
LitPatternAST = namedtuple('LitPatternAST', 'val')
DataPatternAST = namedtuple('TypePatternAST', 'name, items')

NameAST = namedtuple('NameAST', 'name')
NumAST = namedtuple('NumAST', 'val')
TupleAST = namedtuple('TupleAST', 'items')
TypeAST = namedtuple('TypeAST', 'name, constructors')
ConstructorAST = namedtuple('ConstructorAST', 'name, type_constructor, items')