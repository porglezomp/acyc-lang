import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('/path/to/ptdraft/')

import nose
import functools

def exfail(test):
    @functools.wraps(test)
    def inner(*args, **kwargs):
        try:
            test(*args, **kwargs)
        except Exception:
            raise nose.SkipTest
        else:
            raise AssertionError("Failure expected")
    return inner
