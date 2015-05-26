from llvm import *
from llvm.core import *
from env import Env
import acycast
from pprint import pprint

def codegen(ast):
    module = Module.new('module')
    env = Env()

    # Only handle the functions
    functions = [item for item in ast if item.isa(acycast.FnAST)]

    # Move all the functions with the same names into a list
    fn_env = {}
    for fn in functions:
        if fn.name not in fn_env:
            fn_env[fn.name] = []
        fn_env[fn.name].append(fn)

    # Desugar by merging all top level function cases into one function
    # with a `match` inside it
    functions = [merge_functions(fn_list) for fn_list in fn_env.values()]

    # Forward declare all functions for use in codegen
    for fn in functions:
        env[fn.name] = decl_function(fn, module)

    # Generate the code for all the functions
    for fn in functions:
        env[fn.name] = fn.codegen(env, module)

    return module

def merge_functions(fn_list):
    if len(fn_list) == 1:
        return fn_list[0]
    cases = [acycast.CaseAST(fn.pattern, fn.body) for fn in fn_list]
    name = fn_list[0].name
    pattern = acycast.LitPatternAST('_n')
    body = acycast.MatchAST(pattern, cases)
    fn = acycast.FnAST(name, pattern, body)
    print(fn)
    return fn

def decl_function(ast, module):
    try:
        return module.get_function_named(ast.name)
    except:
        pass

    numtype = Type.double()
    if ast.pattern.isa(acycast.LitPatternAST):
        args = [ast.pattern.val]
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