from aoc2024.utils import sys


def dfs(
    topo_map: list[list[str]],
    ratings: list[list[int]],
    possible_destinations: list[list[set[tuple[int, int]]]],
    root: tuple[int, int],
    pos: tuple[int, int],
    alt: int,
):
    possible_destinations[pos[0]][pos[1]].add(root)
    ratings[pos[0]][pos[1]] += 1
    if alt == 0:
        # if we reached a trailhead, we may still want to propagate the possible
        # destinations for other trailheads that might be able to reach this
        # destination
        return
    # Depth First Search to propagate the score to each pos that could have led
    # to the current pos
    rows, cols = len(topo_map), len(topo_map[0])
    for dir in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
        i, j = pos[0] + dir[0], pos[1] + dir[1]
        if 0 <= i < rows and 0 <= j < cols and topo_map[i][j] == str(alt - 1):
            dfs(topo_map, ratings, possible_destinations, root, (i, j), alt - 1)


def main():
    inp = sys.stdin.read()
    topo_map = list(map(list, inp.splitlines()))
    # find all trailheads (0)
    trail_heads = []
    nines = []
    rows, cols = len(topo_map), len(topo_map[0])
    for i in range(rows):
        for j in range(cols):
            if topo_map[i][j] == "0":
                trail_heads.append((i, j))
            if topo_map[i][j] == "9":
                nines.append((i, j))
    # we can start from 9s and work our way backwards.
    # this way we can simply propagate (with += 1) the score of each cell,
    # and we can in particular extract the one of the trailheads.
    # possible_destinations = [[0] * cols for _ in range(rows)]
    possible_destinations = [[set() for _ in range(cols)] for _ in range(rows)]
    ratings = [[0] * cols for _ in range(rows)]
    for pos in nines:
        dfs(topo_map, ratings, possible_destinations, pos, pos, 9)

    # find the score of each trailhead
    print("part 1:", sum(len(possible_destinations[pos[0]][pos[1]]) for pos in trail_heads))
    print("part 2:", sum(ratings[pos[0]][pos[1]] for pos in trail_heads))


if __name__ == "__main__":
    main()
