from aoc2024.utils import ic, deque, print_grid, defaultdict, deepcopy


def shortest_path(grid: list[list[str]]):
    rows, cols = len(grid), len(grid[0])
    start = (0, 0)
    end = (rows - 1, cols - 1)
    # run BFS
    queue: deque[tuple[int, int]] = deque([start])
    dist = [[-1 for _ in range(cols)] for _ in range(rows)]
    dist[0][0] = 0
    prev: defaultdict[tuple[int, int], tuple[int, int]] = defaultdict(lambda: (-1, -1))
    while queue:
        p = queue.popleft()
        d = dist[p[0]][p[1]]
        if p == end:
            # grid = deepcopy(grid)
            # while prev[p] != (-1, -1):
            #     grid[p[0]][p[1]] = "O"
            #     p = prev[p]
            # grid[p[0]][p[1]] = "O"
            # print_grid(grid, True)
            return d
        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            next_p = (p[0] + direction[0], p[1] + direction[1])
            if (0 <= next_p[0] < rows and 0 <= next_p[1] < cols) and (grid[next_p[0]][next_p[1]] == ".") and (dist[next_p[0]][next_p[1]] == -1):
                dist[next_p[0]][next_p[1]] = d + 1
                prev[next_p] = p
                queue.append(next_p)
    return -1


def main():
    inp = open("data/18.txt", "r").read()
    rows, cols, n_coords = 71, 71, 1024
    # inp = open("data/18bis.txt", "r").read()
    # rows, cols, n_coords = 7, 7, 12
    coords = list(map(lambda s: (int(s[: s.find(",")]), int(s[s.find(",") + 1 :])), inp.splitlines()))
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    for coord in coords[:n_coords]:
        grid[coord[0]][coord[1]] = "#"
    # print_grid(grid, True)
    print("part 1:", (s := shortest_path(grid)))
    while s != -1:
        grid[coords[n_coords][0]][coords[n_coords][1]] = "#"
        n_coords += 1
        # print_grid(grid, True)
        s = shortest_path(grid)
    print("part 2:", coords[n_coords - 1])
