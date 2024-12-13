from copy import deepcopy
from typing import Literal, get_args
from aoc2024.utils import sys, timeit, deque, product, wraps, partial, dataclass
from itertools import count


def main():
    inp = sys.stdin.read()
    grid = list(map(list, inp.splitlines()))

    @wraps(print)
    def vprint(*args, **kwargs):
        if len(grid) < 15:
            print(*args, **kwargs)

    rows, cols = len(grid), len(grid[0])
    regions = [[-1] * cols for _ in range(rows)]
    areas: list[list[tuple[int, int]]] = []
    perimeters: list[int] = []
    chars: list[str] = []
    for i, j in product(range(rows), range(cols)):
        vprint(f"Starting in i={i}, j={j}", end="")
        if regions[i][j] == -1:
            c = grid[i][j]
            chars.append(c)
            areas.append([])
            perimeters.append(0)
            region_idx = len(chars) - 1
            vprint(f" starting flood fill for region {region_idx} (char {grid[i][j]})")
            q = deque([(i, j)])
            while q:
                i, j = q.popleft()
                vprint(f"flooding i={i}, j={j}")
                if regions[i][j] == -1:  # even if we only add to the queue cells that were not visited, we may do it twice if
                    regions[i][j] = region_idx
                    areas[-1].append((i, j))
                    perimeters[-1] += 4
                    for idir, jdir in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
                        if 0 <= (inew := i + idir) < rows and 0 <= (jnew := j + jdir) < cols and grid[inew][jnew] == c:
                            if regions[inew][jnew] == -1:
                                q.append((inew, jnew))
                            else:
                                perimeters[-1] -= 2  # fence on the interior, counted for this cell and the other

        else:
            vprint(f" region {regions[i][j]} (char {grid[i][j]}) already visited")

    vprint(grid, regions, chars, areas, perimeters)
    print("part 1", sum(p * len(a) for p, a in zip(perimeters, areas)))

    # in each component, we can
    new_perimeters: list[int] = []
    for area in areas:
        # sort points by row, and then by col
        sorted_area = sorted(area)
        i, j = sorted_area[0]
        vprint(f"sorted points for region {regions[i][j]} (char {grid[i][j]}): {sorted_area}")
        per = 0
        for i, j in sorted_area:
            left = 1 <= j and regions[i][j] == regions[i][j - 1]
            left_up = 1 <= i and 1 <= j and regions[i][j] == regions[i - 1][j - 1]
            up = 1 <= i and regions[i][j] == regions[i - 1][j]
            right_up = 1 <= i and j < cols - 1 and regions[i][j] == regions[i - 1][j + 1]
            if (
                # ... OR A.. OR A.A OR ..A
                # .A     .A     .A     .A
                (not left and not up)
                # AAA
                # .A
                or (not left and left_up and up and right_up)
            ):
                per += 4
            elif (
                # AA.
                # .A
                (not left and left_up and up and not right_up)
                # .AA
                # .A
                or (not left and not left_up and up and right_up)
                # A.. OR A.A
                # AA     AA
                or (left and left_up and not up)
            ):
                per += 2
            elif (
                # .A.
                # AA
                (left and not left_up and up and not right_up)
                # AA.
                # AA
                or (left and left_up and up and not right_up)
            ):
                per -= 2
        new_perimeters.append(per)
        vprint(f"perimeter: {per}")
    print("part 2", sum(p * len(a) for p, a in zip(new_perimeters, areas)))


if __name__ == "__main__":
    main()
