import sys

import numpy as np


def parse_input(inp: str) -> list[list[int]]:
    lines = inp.splitlines()
    return [[int(el) for el in els] for els in [line.split() for line in lines]]


def is_report_valid(report: list[int]) -> bool:
    if len(report) <= 2:
        return True
    diff = np.diff(report)
    return np.all(np.abs(diff) <= 3) and (np.all(diff < 0) or np.all(diff > 0))


def split_report(report: list[int]) -> list[list[int]]:
    return (
        [report[1:]]
        + [report[:i] + report[i + 1 :] for i in range(1, len(report) - 1)]
        + [report[:-1]]
    )


def main2():
    inp = sys.stdin.read()
    reports = parse_input(inp)
    safe = sum(
        is_report_valid(report)
        or any(is_report_valid(split) for split in split_report(report))
        for report in reports
    )
    print(safe)


if __name__ == "__main__":
    main2()
