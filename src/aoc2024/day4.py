from aoc2024.utils import sys, timeit


@timeit
def part1(chars: list[list[str]]):
    nlines = len(chars)
    ncols = len(chars[0])
    # find positions of 'X' in the whole grid
    positions = [(i, j) for i in range(nlines) for j in range(ncols) if chars[i][j] == "X"]
    # no go through each X and try to find all sequences of XMAS
    # in all directions (up, down, left, right, and diagonals)
    found = 0
    for i, j in positions:
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            for k in range(1, 4):
                new_i = i + direction[0] * k
                new_j = j + direction[1] * k
                if new_i < 0 or new_i >= nlines or new_j < 0 or new_j >= ncols:
                    break
                if chars[new_i][new_j] != "MAS"[k - 1]:
                    break
                if k == 3:
                    # print(f"found XMAS at {i},{j}")
                    found += 1

    print(f"part 1: {found}")


@timeit
def part2(chars: list[list[str]]):
    nlines = len(chars)
    ncols = len(chars[0])
    positions = [(i, j) for i in range(nlines) for j in range(ncols) if chars[i][j] == "A"]
    found = 0
    for i, j in positions:
        if (1 <= i < nlines - 1 and 1 <= j < ncols - 1) and (
            sum(
                {chars[i + direction[0]][j + direction[1]], chars[i - direction[0]][j - direction[1]]} == {"M", "S"}
                for direction in [(1, 1), (-1, 1)]
            )
            == 2
        ):
            found += 1

    print(f"part 2: {found}")


def main():
    inp = sys.stdin.read()
    lines = inp.splitlines()
    chars = [list(line) for line in lines]
    part1(chars)
    part2(chars)


if __name__ == "__main__":
    main()
