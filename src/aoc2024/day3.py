from aoc2024.utils import re, sys, timeit


@timeit
def part1(inp: str) -> int:
    mult_pattern = r"mul\((\d+),(\d+)\)"
    part1 = sum(
        int(m.group(1)) * int(m.group(2)) for m in re.finditer(mult_pattern, inp)
    )
    print("part 1: ", part1)


@timeit
def part2(inp: str) -> int:
    mult_pattern = r"mul\((\d+),(\d+)\)"
    # https://regex101.com/r/cqKAV3/1
    to_keep = (
        r"((do\(\)).*?(don't\(\)))|(^(.*?)(?<!do\(\))don't)|(do\(\)(?!don't\(\))(.*?)$)"
    )
    part2 = sum(
        int(m[1]) * int(m[2])
        for kept in re.finditer(to_keep, inp)
        for m in re.finditer(mult_pattern, kept[0])
    )
    print("part 2: ", part2)


def main():
    inp = sys.stdin.read().replace("\n", "")
    part1(inp)
    part2(inp)


if __name__ == "__main__":
    main()
