import math
import os
import sys

import numpy as np


def parse_input(inp: str) -> list[tuple[int, int]]:
    lines = inp.splitlines()
    return [(int(x), int(y)) for x, y in [line.split() for line in lines]]


def main():
    inp = sys.stdin.read()
    numbers = parse_input(inp)
    list1 = [line[0] for line in numbers]
    list2 = [line[1] for line in numbers]
    # sort both lists
    list1.sort()
    list2.sort()
    # find the difference between the two lists
    distance = sum(abs(x - y) for x, y in zip(list1, list2))
    print(distance)


if __name__ == "__main__":
    main()
