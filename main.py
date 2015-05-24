from tokenizer import TokenBuffer, tokenize
from parser import parse

tokens = TokenBuffer(tokenize(open("sample.cy", "r").read()))
print(parse(tokens))
