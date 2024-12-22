from aoc2024.utils import print_grid, sys, parse_grid, heappush, heappop, defaultdict, deepcopy

type grid_t = list[list[str]]
type pos_t = tuple[int, int]


def print_grid_with_path(grid: grid_t, path: list[pos_t]):
    grid = deepcopy(grid)
    for i, j in path:
        grid[i][j] = "O"
    print_grid(grid)


def find_initial_path(grid: grid_t, start: pos_t, end: pos_t):
    path = [start]
    while path[-1] != end:
        for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new = path[-1][0] + dir[0], path[-1][1] + dir[1]
            if grid[new[0]][new[1]] == "." and (len(path) < 2 or new != path[-2]):
                path.append(new)
                break
    return path


shortcut_cache: dict[tuple[pos_t, pos_t], int] = {}


def manhattan(a: pos_t, b: pos_t) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_shortcut(grid: grid_t, start: pos_t, end: pos_t, max_steps: int = 2) -> int:
    """Find shortest path between start and end that only passes via obstacles.
    It uses max_steps to limit the number of steps.
    If it cannot find one, or only paths longer than max_steps are found, it returns -1.
    """
    if (start, end) in shortcut_cache:
        return shortcut_cache[(start, end)]
    rows, cols = len(grid), len(grid[0])
    dist: defaultdict[pos_t, int] = defaultdict(lambda: sys.maxsize)
    dist[start] = 0
    queue = [(0, start)]
    while queue:
        _, curr_pos = heappop(queue)
        # Check if we made it to the end
        if curr_pos == end:
            shortcut_cache[start, end] = dist[end]
            return dist[end]
        # If we alreay reached max_steps, we can't go further
        if dist[curr_pos] == max_steps:
            continue
        # Inspect neighbors and add them to queue
        for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (
                # feasible coord
                0 <= (inew := curr_pos[0] + d[0]) < rows
                and 0 <= (jnew := curr_pos[1] + d[1]) < cols
                # we haven't treated this cell yet
                and (new_pos := (inew, jnew)) not in dist
            ):
                dist[new_pos] = dist[curr_pos] + 1
                heappush(queue, (dist[new_pos] + manhattan(new_pos, end), new_pos))
    return -1


def find_improvements(grid: grid_t, initial_path: list[pos_t], max_steps: int = 2, verbose=False):
    # Now for every pair of points in the path, try cutting from on to the other
    # while only staying on the obstacles and passing by at most 1 cell (other
    # than the start and end).
    improvements: defaultdict[int, int] = defaultdict(lambda: 0)
    for k in range(len(initial_path) - 1):
        for l in range(k + 1, len(initial_path)):
            if manhattan(initial_path[k], initial_path[l]) > max_steps:
                continue
            shortcut_length = find_shortcut(grid, initial_path[k], initial_path[l], max_steps)
            if shortcut_length > 0 and (improvement := l - k - shortcut_length) > 0:
                improvements[improvement] += 1
    if verbose:
        for k, v in sorted(improvements.items()):
            if v == 1:
                print(f"There is one cheat that saves {k} picoseconds.")
            else:
                print(f"There are {v} cheats that save {k} picoseconds.")

    return improvements


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

    initial_path = find_initial_path(grid, start, end)
    initial_time = len(initial_path) - 1
    print(f"Shortest path from {start} to {end} has length {initial_time} picoseconds.")

    print("part 1:", sum(v for k, v in find_improvements(grid, initial_path, 2, True).items() if k >= 100))
    print("part 2:", sum(v for k, v in find_improvements(grid, initial_path, 20, True).items() if k >= 100))


if __name__ == "__main__":
    main()
