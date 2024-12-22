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
from collections import defaultdict, deque
from copy import copy, deepcopy
from functools import cache, lru_cache, partial, wraps
from itertools import combinations, product
from dataclasses import dataclass
from typing import Optional, Callable
from heapq import heappush, heappop

import numpy as np
from icecream import ic


def timeit(f):
    @functools.wraps(f)
    def inner_func(*arg, **kwargs):
        start = time.time_ns()
        result = f(*arg, **kwargs)
        end = time.time_ns()
        print(f"function {f.__name__} took {(end-start)/10e6: .2f} ms")
        return result

    return inner_func


def print_grid(grid: list[list[str]], transpose: bool = False):
    if transpose:
        grid = list(map(list, zip(*grid)))
    for line in grid:
        print("".join(line))
