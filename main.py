from tokenizer import TokenBuffer, tokenize
from parser import parse
from codegen import codegen
from llvm.core import *
from llvm.ee import *

tokens = TokenBuffer(tokenize(open("sample.cy", "r").read()))
ast = parse(tokens)
module = codegen(ast)
ex = ExecutionEngine.new(module, force_interpreter=True)
main = module.get_function_named('main')
result = ex.run_function(main, [])
print(result.as_real(Type.double()))
