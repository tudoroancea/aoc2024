from collections import OrderedDict
from aoc2024.utils import sys, timeit, product, deepcopy, defaultdict, deque, Optional, dataclass

type pos_t = tuple[int, int]


def print_grid(grid: list[list[str]]):
    for line in grid:
        print("".join(line))


@timeit
def part1(grid: list[list[str]], moves: str):
    rows, cols = len(grid), len(grid[0])
    # print("Initial state:")
    # print_grid(grid)

    # find the initial position of the robot
    pos = None
    for i, j in product(range(rows), range(cols)):
        if grid[i][j] == "@":
            pos = i, j
            break
    if pos is None:
        raise ValueError("No starting position found")

    # simulate its movement around the warehouse
    for m in moves:
        dir = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}[m]
        # find the closest cell that is not an obstacle
        first_free_space = pos[0] + dir[0], pos[1] + dir[1]
        while grid[first_free_space[0]][first_free_space[1]] == "O":
            first_free_space = first_free_space[0] + dir[0], first_free_space[1] + dir[1]
        # move pos and obstacles
        if grid[first_free_space[0]][first_free_space[1]] == ".":
            next_pos = pos[0] + dir[0], pos[1] + dir[1]
            grid[pos[0]][pos[1]] = "."
            grid[next_pos[0]][next_pos[1]] = "@"
            if first_free_space != next_pos:
                grid[first_free_space[0]][first_free_space[1]] = "O"
            pos = next_pos
        # print new grid
        # print(f"Move {m}:")
        # print_grid(grid)

    # find coordinates of all obstacles
    print("part 1:", sum(100 * i + j for i, j in product(range(rows), range(cols)) if grid[i][j] == "O"))


@dataclass
class Node:
    left: Optional[pos_t]
    right: Optional[pos_t]


@timeit
def part2(grid: list[list[str]], moves: str):
    # create new grid with double width
    new_grid = [[""] * 2 * len(grid[0]) for _ in range(len(grid))]
    for i, j in product(range(len(grid)), range(len(grid[0]))):
        match grid[i][j]:
            case ".":
                new_grid[i][2 * j] = "."
                new_grid[i][2 * j + 1] = "."
            case "@":
                new_grid[i][2 * j] = "@"
                new_grid[i][2 * j + 1] = "."
            case "O":
                new_grid[i][2 * j] = "["
                new_grid[i][2 * j + 1] = "]"
            case "#":
                new_grid[i][2 * j] = "#"
                new_grid[i][2 * j + 1] = "#"
    grid = new_grid
    rows, cols = len(grid), len(grid[0])

    print("Initial state:")
    print_grid(grid)

    # find the initial position of the robot
    pos = None
    for i, j in product(range(rows), range(cols)):
        if grid[i][j] == "@":
            pos = i, j
            break
    if pos is None:
        raise ValueError("No starting position found")

    # simulate its movement around the warehouse
    for m in moves:
        dir = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}[m]

        if dir[0] == 0:
            # move horizontally => easy collision detection
            # find the closest cell that is not an obstacle
            k = 1
            while grid[pos[0]][pos[1] + k * dir[1]] in {"[", "]"}:
                k += 1
            assert k % 2 == 1
            # move pos and obstacles
            if grid[pos[0]][pos[1] + k * dir[1]] == ".":
                for r in range(k, 0, -1):
                    grid[pos[0]][pos[1] + r * dir[1]] = grid[pos[0]][pos[1] + (r - 1) * dir[1]]
                grid[pos[0]][pos[1]] = "."
                pos = (pos[0], pos[1] + dir[1])
        else:
            # move vertically => hard collision detection
            if (c := grid[pos[0] + dir[0]][pos[1]]) == ".":
                grid[pos[0] + dir[0]][pos[1]] = "@"
                grid[pos[0]][pos[1]] = "."
                pos = pos[0] + dir[0], pos[1]
            elif c in {"[", "]"}:
                tree: dict[pos_t, Node] = defaultdict(lambda: Node(None, None))
                # we have to construct a binary tree, with each node representing a box. We store the nodes as a dict with keys corresponding to the pos of "["
                # As we construct it, if we a certain box doesn't have anything in front of it, we stop exploring from this node and consider it a leaf.
                # If one has an obstacle in front of it, we stop everything because we won't be able to move.
                # If we traversed all the graph and nothing is blocking, we can sort the nodes by i coordinate, and then move them in reverse order
                q: deque[pos_t] = deque([(pos[0] + dir[0], pos[1] - int(c == "]"))])
                cant_move = False
                while q:
                    # breakpoint()
                    i, j = q.popleft()
                    tree[(i, j)]
                    if (left := grid[i + dir[0]][j]) == (right := grid[i + dir[0]][j + 1]) == ".":
                        # nothing in front
                        continue
                    elif left == "[" and right == "]":
                        # a single other box in front
                        q.append((i + dir[0], j))
                        tree[(i, j)].left = tree[(i, j)].right = (i + dir[0], j)
                    elif left == "#" or right == "#":
                        # an obstacls is blocking
                        cant_move = True
                        break
                    else:
                        if left == "]":
                            q.append((i + dir[0], j - 1))
                            tree[(i, j)].left = (i + dir[0], j - 1)
                        if right == "[":
                            q.append((i + dir[0], j + 1))
                            tree[(i, j)].right = (i + dir[0], j + 1)
                if cant_move:
                    continue
                # NOW MOVE THE BOXES
                # construct the ordered list of boxes to move
                boxes = [k for k in sorted(tree.keys(), key=lambda x: x[0], reverse=m == "v")]
                for i, j in boxes:
                    assert grid[i + dir[0]][j] == "."
                    assert grid[i + dir[0]][j + 1] == ".", f"{grid[i + dir[0]][j + 1]}"
                    assert grid[i][j] == "["
                    assert grid[i][j + 1] == "]"
                    grid[i + dir[0]][j] = "["
                    grid[i + dir[0]][j + 1] = "]"
                    grid[i][j] = "."
                    grid[i][j + 1] = "."

                # AND MOVE THE ROBOT
                grid[pos[0] + dir[0]][pos[1]] = "@"
                grid[pos[0]][pos[1]] = "."
                pos = pos[0] + dir[0], pos[1]

        # print(f"After move {m}:")
        # print_grid(grid)

    # find coordinates of all obstacles
    print("part 2:", sum(100 * i + j for i, j in product(range(rows), range(cols)) if grid[i][j] == "["))


def main():
    # inp = sys.stdin.read().splitlines()
    with open("data/15.txt") as f:
        inp = f.read().splitlines()
    sep = inp.index("")
    grid = list(map(list, inp[:sep]))
    moves = "".join(inp[sep + 1 :])
    part1(deepcopy(grid), moves)
    part2(deepcopy(grid), moves)
