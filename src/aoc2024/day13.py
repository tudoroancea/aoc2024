from aoc2024.utils import sys, re, timeit
# import numpy as np t


def solve_machine(button_a: tuple[int, int], button_b: tuple[int, int], goal: tuple[int, int]) -> int:
    det = button_a[0] * button_b[1] - button_a[1] * button_b[0]
    if det == 0:
        return 0
    # Solve linear system with Cramer's rule (https://en.wikipedia.org/wiki/Cramer%27s_rule)
    alpha = (goal[0] * button_b[1] - goal[1] * button_b[0]) / det
    beta = (button_a[0] * goal[1] - button_a[1] * goal[0]) / det
    if abs(alpha % 1.0) < 1e-6 and abs(beta % 1.0) < 1e-6:
        return 3 * int(alpha) + int(beta)
    else:
        return 0


@timeit
def part1(inp: str):
    print(
        "part 1:",
        sum(
            solve_machine((int(match[1]), int(match[2])), (int(match[3]), int(match[4])), (int(match[5]), int(match[6])))
            for match in re.finditer(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)", inp)
        ),
    )


@timeit
def part2(inp: str):
    print(
        "part 2:",
        sum(
            solve_machine(
                (int(match[1]), int(match[2])), (int(match[3]), int(match[4])), (int(match[5]) + 10000000000000, int(match[6]) + 10000000000000)
            )
            for match in re.finditer(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)", inp)
        ),
    )


def main():
    inp = sys.stdin.read()
    part1(inp)
    part2(inp)
