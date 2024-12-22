from aoc2024.utils import defaultdict, heappop, heappush

type node = tuple[int, int, str]

orientations = ["E", "N", "W", "S"]
directions = {"E": (0, 1), "N": (-1, 0), "W": (0, -1), "S": (1, 0)}


def dijkstra(grid: list[list[str]], start: node, goal: node):
    q: list[tuple[float, node]] = [(0, start)]
    dist: defaultdict[node, float] = defaultdict(lambda: float("inf"))
    dist[start] = 0
    paths: defaultdict[node, list[list[node]]] = defaultdict(list)
    paths[start] = [[start]]
    while q:
        curr_dist, curr_node = heappop(q)
        if curr_dist > dist[curr_node]:
            continue
        for d, next_node in [
            (1000, curr_node[:2] + (orientations[(orientations.index(curr_node[2]) + 1) % len(orientations)],)),
            (1000, curr_node[:2] + (orientations[(orientations.index(curr_node[2]) - 1) % len(orientations)],)),
            (1, (curr_node[0] + (dir := directions[curr_node[2]])[0], curr_node[1] + dir[1], curr_node[2])),
        ]:
            if grid[next_node[0]][next_node[1]] == ".":
                next_dist = dist[curr_node] + d
                if next_dist < dist[next_node]:
                    dist[next_node] = next_dist
                    heappush(q, (dist[next_node], next_node))
                    paths[next_node] = [path + [next_node] for path in paths[curr_node]]
                elif next_dist == dist[next_node]:
                    paths[next_node].extend(path + [next_node] for path in paths[curr_node])

    return dist[goal], paths[goal]


def main():
    with open("data/16.txt") as f:
        data = f.read().splitlines()
    grid = list(map(list, data))
    rows, cols = len(grid), len(grid[0])
    start = (rows - 2, 1)
    end = (1, cols - 2)
    grid[start[0]][start[1]] = "."
    grid[end[0]][end[1]] = "."
    results = [dijkstra(grid, start + ("E",), end + (o,)) for o in orientations]
    m = min(res[0] for res in results)
    print("part 1:", m)
    shortest_paths_cells = set().union(*[set().union(*res[1]) for res in results])
    print("part 2:", len(set(p[:2] for p in shortest_paths_cells)))


if __name__ == "__main__":
    main()
