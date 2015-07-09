from collections import namedtuple
from llvm import *
from llvm.core import *
from env import Env
from acycexceptions import *
from codegen import decl_function


class AST:
    def __repr__(self):
        name = self.__class__.__name__
        _code = self.__init__.__code__
        args = _code.co_varnames[1:_code.co_argcount]
        args = [repr(self.__dict__[x]) for x in args]
        return "{}({})".format(name, ", ".join(args))

    def isa(self, item):
        return isinstance(self, item)


class BinopAST (AST):
    def __init__(self, lhs, op, rhs):
        self.lhs, self.op, self.rhs = lhs, op, rhs

    def codegen(self, env, module, builder):
        left = self.lhs.codegen(env, module, builder)
        right = self.rhs.codegen(env, module, builder)
        if self.op == "+":
            return builder.fadd(left, right, 'addtmp')
        elif self.op == "-":
            return builder.fsub(left, right, 'subtmp')
        elif self.op == "*":
            return builder.fmul(left, right, 'multmp')
        elif self.op == "/":
            return builder.fdiv(left, right, 'divtmp')
        elif self.op == "==":
            result = builder.fcmp(FCMP_UEQ, left, right, 'cmptmp')
            return builder.uitofp(result, Type.double(), 'booltmp')


class FnAST (AST):
    def __init__(self, name, pattern, body):
        self.name, self.pattern, self.body = name, pattern, body

    def codegen(self, env, module, builder=None):
        function = decl_function(self, module)
        fnenv = Env(env)
        for arg in function.args:
            fnenv[arg.name] = arg
        bb = function.append_basic_block('entry')
        builder = Builder.new(bb)
        result = self.body.codegen(fnenv, module, builder)
        builder.ret(result)

        function.verify()
        return function


class FnCallAST (AST):
    def __init__(self, name, arg):
        self.name, self.arg = name, arg

    def codegen(self, env, module, builder):
        function = env[self.name]
        if function is None:
            raise RuntimeError("Undefined function `{}`".format(
                self.name
            ))

        if self.arg.isa(TupleAST):
            m, b = module, builder
            args = [item.codegen(env, m, b) for item in self.arg.items]
        else:
            args = [self.arg.codegen(env, module, builder)]

        return builder.call(function, args, 'calltmp')



class IfElseAST (AST):
    def __init__(self, cond, true, false):
        self.cond, self.true, self.false = cond, true, false

    def codegen(self, env, module, builder):
        cond = self.cond.codegen(env, module, builder)
        cond = builder.fcmp(FCMP_ONE, cond,
                            Constant.real(Type.double(), 0), 'ifcond')
        function = builder.basic_block.function
        then_block = function.append_basic_block('true')
        else_block = function.append_basic_block('else')
        merge_block = function.append_basic_block('ifcond')

        builder.cbranch(cond, then_block, else_block)
        builder.position_at_end(then_block)
        then_value = self.true.codegen(env, module, builder)
        builder.branch(merge_block)

        then_block = builder.basic_block

        builder.position_at_end(else_block)
        else_value = self.false.codegen(env, module, builder)
        builder.branch(merge_block)

        else_block = builder.basic_block

        builder.position_at_end(merge_block)

        phi = builder.phi(Type.double(), 'iftmp')
        phi.add_incoming(then_value, then_block)
        phi.add_incoming(else_value, else_block)

        return phi



class MatchAST (AST):
    def __init__(self, expr, cases):
        self.expr, self.cases = expr, cases


class CaseAST (AST):
    def __init__(self, pattern, body):
        self.pattern, self.body = pattern, body


class LetAST (AST):
    def __init__(self, binds, body):
        self.binds, self.body = binds, body


class PatternAST (AST):
    def __init__(self, pattern):
        self.pattern = pattern


class TuplePatternAST (AST):
    def __init__(self, patterns):
        self.patterns = patterns

CondPatternAST = namedtuple('CondPatternAST', 'cond')

class LitPatternAST (PatternAST):
    def __init__(self, val):
        PatternAST.__init__(self, val)
        self.val = val

DataPatternAST = namedtuple('TypePatternAST', 'name, items')

class NameAST (AST):
    def __init__(self, name):
        self.name = name

    def codegen(self, env, module, builder):
        return env[self.name]

class NumAST (AST):
    def __init__(self, val):
        self.val = val

    def codegen(self, env, module, builder):
        return Constant.real(Type.double(), self.val)


class TupleAST (AST):
    def __init__(self, items):
        self.items = items

class UnitAST (AST):
    def __init__(self): pass

TypeAST = namedtuple('TypeAST', 'name, type_constructor, constructors')
ConstructorAST = namedtuple('ConstructorAST', 'name, items')
