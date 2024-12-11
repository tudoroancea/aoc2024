# ruff: noqa: F401
import collections
import functools
import math
import multiprocessing
import os
import re
import sys
import time

# some useful functions or classes that we import directly
from collections import defaultdict
from copy import copy, deepcopy
from itertools import combinations, product

import numpy as np


def timeit(f):
    @functools.wraps(f)
    def inner_func(*arg, **kwargs):
        start = time.time_ns()
        result = f(*arg, **kwargs)
        end = time.time_ns()
        print(f"function {f.__name__} took {(end-start)/10e6: .2f} ms")
        return result

    return inner_func
