import harness
import nose
import random

import tokenizer

def test_tokenize_zero():
    num = next(tokenizer.tokenize("0"))
    nose.tools.assert_equal(num, tokenizer.Num(0, 0, 0))

def test_tokenize_naturals():
    for _ in range(1000):
        n = random.randint(0, 1000000000)
        num = next(tokenizer.tokenize(str(n)))
        nose.tools.assert_equal(num, tokenizer.Num(n, 0, 0))

@harness.exfail
def test_tokenize_negatives():
    for _ in range(1000):
        n = random.randint(-1000000000, 0)
        num = next(tokenizer.tokenize(str(n)))
        nose.tools.assert_equal(num, tokenizer.Num(n, 0, 0))

def test_tokenize_positive_floats():
    for _ in range(1000):
        n = random.random() * 1000000000
        num = next(tokenizer.tokenize('{:.12f}'.format(n)))
        nose.tools.assert_equal(num, tokenizer.Num(n, 0, 0))

@harness.exfail
def test_tokenize_negative_floats():
    for _ in range(1000):
        n = random.random() * -1000000000
        num = next(tokenizer.tokenize('{:.12f}'.format(n)))
        nose.tools.assert_equal(num, tokenizer.Num(n, 0, 0))

def test_tokenize_exponential_notation():
    for _ in range(1000):
        n = random.random() * 1e32
        num = next(tokenizer.tokenize('{:.12e}'.format(n)))
        nose.tools.assert_equal(num, tokenizer.Num(n, 0, 0))
