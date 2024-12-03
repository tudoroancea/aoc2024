import sys

import numpy as np


def parse_input(inp: str) -> list[list[int]]:
    lines = inp.splitlines()
    return [[int(el) for el in els] for els in [line.split() for line in lines]]


def main():
    inp = sys.stdin.read()
    reports = parse_input(inp)
    safe = []
    for report in reports:
        diff = np.diff(report)
        safe.append(
            np.all(np.abs(diff) <= 3) and (np.all(diff < 0) or np.all(diff > 0))
        )
    print(sum(safe))


if __name__ == "__main__":
    main()
