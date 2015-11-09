import harness
import nose
import random

import tokenizer
from decimal import *
getcontext().prec = 64

def test_tokenize_zero():
    num = next(tokenizer.tokenize('0'))
    nose.tools.assert_equal(num, tokenizer.Num(0, 0, 0))

def test_tokenize_1_23():
    num = next(tokenizer.tokenize('1.23'))
    nose.tools.assert_equal(num, tokenizer.Num(Decimal('1.23'), 0, 0))

def test_tokenize_naturals():
    for _ in range(1000):
        n = random.randint(0, 1000000000)
        num = next(tokenizer.tokenize(str(n)))
        nose.tools.assert_equal(num, tokenizer.Num(n, 0, 0))

def test_tokenize_negatives():
    for _ in range(1000):
        n = random.randint(-1000000000, 0)
        tok = tokenizer.tokenize(str(n))
        sign, num = next(tok), next(tok)
        nose.tools.assert_equal(sign, tokenizer.Op('-', 0, 0))
        nose.tools.assert_equal(num, tokenizer.Num(-n, 0, 0))

def test_tokenize_positive_floats():
    for _ in range(1000):
        n = random.random() * 1000000000
        num = next(tokenizer.tokenize('{}'.format(Decimal(n))))
        nose.tools.assert_equal(num, tokenizer.Num(Decimal(n), 0, 0))

def test_tokenize_negative_floats():
    for _ in range(1000):
        n = random.random() * -1000000000
        tok = tokenizer.tokenize('{}'.format(Decimal(n)))
        sign, num = next(tok), next(tok)
        nose.tools.assert_equal(sign, tokenizer.Op('-', 0, 0))
        nose.tools.assert_equal(num, tokenizer.Num(-Decimal(n), 0, 0))

@harness.exfail
def test_tokenize_exponential_notation():
    for _ in range(1000):
        n = random.random() * 1e32
        num = next(tokenizer.tokenize('{:.32e}'.format(n)))
        nose.tools.assert_equal(num, tokenizer.Num(n, 0, 0))
