from itertools import combinations
from collections import defaultdict
from aoc2024.utils import sys


def main():
    inp = sys.stdin.read()
    lines = inp.splitlines()
    grid = list(map(list, lines))
    rows, cols = len(grid), len(grid[0])

    def in_grid(i, j):
        return 0 <= i < rows and 0 <= j < cols

    # first find all sets of frequencies
    antennas_per_freq = defaultdict(set)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != ".":
                antennas_per_freq[grid[i][j]].add((i, j))
    # find for each frequency, all the antinodes
    antinodes = set()
    for freq, positions in antennas_per_freq.items():
        for pos1, pos2 in combinations(positions, 2):
            dir = (pos2[0] - pos1[0], pos2[1] - pos1[1])
            antinode1 = (pos2[0] + dir[0], pos2[1] + dir[1])
            antinode2 = (pos1[0] - dir[0], pos1[1] - dir[1])
            if in_grid(*antinode1):
                antinodes.add(antinode1)
            if in_grid(*antinode2):
                antinodes.add(antinode2)
    print("part 1: ", len(antinodes))

    # find new antinodes based on harmonics
    antinodes_harmonics = set()
    for freq, positions in antennas_per_freq.items():
        for pos1, pos2 in combinations(positions, 2):
            dir = (pos2[0] - pos1[0], pos2[1] - pos1[1])
            for sign in {-1, 1}:
                for i in range(max(rows, cols) + 1):
                    antinode = (pos1[0] + sign * dir[0] * i, pos1[1] + sign * dir[1] * i)
                    if in_grid(*antinode):
                        antinodes_harmonics.add(antinode)
                    else:
                        # the following ones will not be in the grid either,
                        # so we can break early
                        break
    print("part 2: ", len(antinodes_harmonics))


if __name__ == "__main__":
    main()
