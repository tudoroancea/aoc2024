from aoc2024.utils import sys, timeit
from functools import cache


@cache
def count_stones(stone: int, depth: int):
    if depth == 0:
        return 1
    if stone == 0:
        return count_stones(1, depth - 1)
    elif (l := len((s := str(stone)))) % 2 == 0:
        return count_stones(int(s[: l // 2]), depth - 1) + count_stones(int(s[l // 2 :]), depth - 1)
    else:
        return count_stones(2024 * stone, depth - 1)


@timeit
def part1(stones: list[int]):
    print("part 1: ", sum(count_stones(stone, 25) for stone in stones))


@timeit
def part2(stones: list[int]):
    print("part 2: ", sum(count_stones(stone, 75) for stone in stones))


def main():
    inp = sys.stdin.read().strip()
    stones = list(map(int, inp.split()))
    part1(stones)
    part2(stones)


if __name__ == "__main__":
    main()
