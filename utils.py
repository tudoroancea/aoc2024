import functools
import math
import os
import re
import sys
import time


def timeit(f):
    @functools.wraps(f)
    def inner_func(*arg, **kwargs):
        start = time.time_ns()
        result = f(*arg, **kwargs)
        end = time.time_ns()
        print(f"function {f.__name__} took {(end-start)/10e6: .2f} ms")
        return result

    return inner_func
