from aoc2024.utils import sys, print_grid, parse_grid, heappush, heappop, defaultdict

type grid_t = list[list[str]]
type pos_t = tuple[int, int]


def find_shortest_path(grid: grid_t, start: pos_t, end: pos_t) -> list[pos_t]:
    rows, cols = len(grid), len(grid[0])
    # a* search using manhattan distance as heuristic
    # https://en.wikipedia.org/wiki/A*_search_algorithm
    queue = [(0, start)]
    dist: defaultdict[pos_t, int] = defaultdict(lambda: sys.maxsize)
    prev: defaultdict[pos_t, pos_t] = defaultdict(lambda: (-1, -1))
    while queue:
        _, pos = heappop(queue)
        if pos == end:
            # reconstruct path
            path = [pos]
            while prev[pos] != (-1, -1):
                path.append(prev[pos])
                pos = prev[pos]
            path.reverse()
            return path
        for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if 0 <= (inew := pos[0] + d[0]) < rows and 0 <= (jnew := pos[1] + d[1]) < cols and grid[inew][jnew] == "." and (inew, jnew) not in dist:
                dist[inew, jnew] = dist[pos] + 1
                prev[inew, jnew] = pos
                heappush(queue, (dist[inew, jnew] + abs(inew - end[0]) + abs(jnew - end[1]), (inew, jnew)))
    return []


def main():
    # data = "data/20bis.txt"
    data = "data/20.txt"
    with open(data, "r") as f:
        lines = f.readlines()
    grid = parse_grid(lines)
    rows, cols = len(grid), len(grid[0])

    # find start and end
    start = None
    end = None
    for i in range(rows):
        for j in range(cols):
            if start is not None and end is not None:
                break
            if start is None and grid[i][j] == "S":
                start = (i, j)
                grid[i][j] = "."
            if end is None and grid[i][j] == "E":
                end = (i, j)
                grid[i][j] = "."
    if start is None or end is None:
        return

    path = find_shortest_path(grid, start, end)
    original_time = len(path) - 1
    print(f"Shortest path from {start} to {end} has length {original_time}ps")

    # From every point throughout the path, try cheating.
    # Each cheating tentative is made of an obstacle position (k,l) that we remove from the grid.
    # The only obstacles that should lead to improvements are along the path we already have.

    def cheat(obstacle: pos_t) -> int:
        grid[obstacle[0]][obstacle[1]] = "."
        shorter_path = find_shortest_path(grid, start, end)
        time = len(shorter_path) - 1
        grid[obstacle[0]][obstacle[1]] = "#"
        return time

    cheats: defaultdict[pos_t, int] = defaultdict(lambda: 0)
    for p in path:
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (
                0 <= (inew := p[0] + direction[0]) < rows
                and 0 <= (jnew := p[1] + direction[1]) < cols
                and grid[inew][jnew] == "#"
                and (inew, jnew) not in cheats
            ):
                cheats[(inew, jnew)] = original_time - cheat((inew, jnew))
    # aggregate number of different cheats per improvement
    improvements = {v: 0 for k, v in cheats.items() if v > 0}
    for k, v in cheats.items():
        if v > 0:
            improvements[v] += 1
    # print(f"Cheats per improvement: {improvements}")
    for k, v in sorted(improvements.items()):
        if v == 1:
            print(f"There is one cheat that saves {k} picoseconds.")
        else:
            print(f"There are {v} cheats that save {k} picoseconds.")
    print("part 1:", sum(v for k, v in improvements.items() if k >= 100))


if __name__ == "__main__":
    main()
