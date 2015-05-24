from llvm import *
from llvm.core import *
from env import Env
import acycast

def codegen(ast):
    module = Module.new('module')
    env = Env()

    functions = [item for item in ast if item.isa(acycast.FnAST)]
    for fn in functions:
        env[fn.name] = decl_function(fn, module)
    for fn in functions:
        env[fn.name] = fn.codegen(env, module)

    return module

def decl_function(ast, module):
    try:
        return module.get_function_named(ast.name)
    except:
        pass

    numtype = Type.double()
    if ast.pattern.isa(acycast.LitPatternAST):
        args = (ast.pattern.val,)
    elif ast.pattern.isa(acycast.TuplePatternAST):
        args = [item.val for item in ast.pattern.patterns]
    elif ast.pattern.isa(acycast.UnitAST):
        args = []
    else:
        unimplemented("something not lit or tuple")

    fntype = Type.function(numtype, [numtype for _ in args])
    function = module.add_function(fntype, ast.name)
    for fnarg, argname in zip(function.args, args):
        fnarg.name = argname

    return function