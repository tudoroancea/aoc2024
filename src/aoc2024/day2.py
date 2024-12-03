from aoc2024.utils import np, sys, timeit


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


@timeit
def part1(reports: list[list[int]]):
    print("part 1: ", sum(is_report_valid(report) for report in reports))


@timeit
def part2(reports: list[list[int]]):
    print(
        "part 2: ",
        sum(
            is_report_valid(report)
            or any(is_report_valid(split) for split in split_report(report))
            for report in reports
        ),
    )


def main():
    inp = sys.stdin.read()
    reports = parse_input(inp)
    part1(reports)
    part2(reports)


if __name__ == "__main__":
    main()
