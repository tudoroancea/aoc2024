from collections import deque
from copy import deepcopy

from aoc2024.utils import sys, timeit


def print_grid(grid: list[list[str]]):
    print(" 0123456789")
    for i, line in enumerate(grid):
        print(f"{i}", end="")
        for j, char in enumerate(line):
            print(f"{char}", end="")
        print()


def grid_travel(grid: list[list[str]], pos: tuple[int, int], dir: tuple[int, int]):
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    directions_char = ["↑", "→", "↓", "←"]

    def exiting(dir: tuple[int, int], pos: tuple[int, int]):
        i, j = pos
        match dir:
            case (0, 1):
                return j == cols - 1
            case (1, 0):
                return i == rows - 1
            case (0, -1):
                return j == 0
            case (-1, 0):
                return i == 0

    visited = [pos]
    while not exiting(dir, pos):
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if grid[next_pos[0]][next_pos[1]] in ["."] + directions_char:
            # count the cell if it wasnt visited yet
            if grid[next_pos[0]][next_pos[1]] == ".":
                visited.append(next_pos)
            elif grid[next_pos[0]][next_pos[1]] == directions_char[directions.index(dir)]:
                # we are in a loop
                # print_grid(grid)
                return visited, True
            # mark it as visited
            grid[pos[0]][pos[1]] = directions_char[directions.index(dir)]
            # the space is empty, move to it
            pos = next_pos
        elif grid[next_pos[0]][next_pos[1]] == "#":
            # the space is a wall, change direction
            dir = directions[(directions.index(dir) + 1) % 4]
    # mark last cell as visited
    grid[pos[0]][pos[1]] = directions_char[directions.index(dir)]
    # print_grid(grid)
    return visited, False


def grid_travel_2(grid: list[list[str]], pos: tuple[int, int], dir: tuple[int, int]):
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    directions_char = ["↑", "→", "↓", "←"]

    def exiting(dir: tuple[int, int], pos: tuple[int, int]):
        i, j = pos
        match dir:
            case (0, 1):
                return j == cols - 1
            case (1, 0):
                return i == rows - 1
            case (0, -1):
                return j == 0
            case (-1, 0):
                return i == 0

    visited = [pos]
    obstacles = 0
    while not exiting(dir, pos):
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if grid[next_pos[0]][next_pos[1]] in ["."] + directions_char:
            # if the next pos has already a direction which is the current one,
            # we are in a loop
            # if grid[next_pos[0]][next_pos[1]] == directions_char[directions.index(dir)]:
            #     return visited, True
            # count the cell if it wasnt visited yet
            if grid[next_pos[0]][next_pos[1]] == ".":
                visited.append(next_pos)
            # mark it as visited
            grid[pos[0]][pos[1]] = directions_char[directions.index(dir)]
            # check if introducing an obstacle at next pos leads to a loop
            new_grid = deepcopy(grid)
            _, loop = grid_travel(new_grid, pos, dir)
            if loop:
                obstacles += 1
            # update next pos
            pos = next_pos
        elif grid[next_pos[0]][next_pos[1]] == "#":
            # the space is a wall, change direction
            dir = directions[(directions.index(dir) + 1) % 4]
    # mark last cell as visited
    grid[pos[0]][pos[1]] = directions_char[directions.index(dir)]
    # print_grid(grid)
    return visited, obstacles


def main():
    inp = sys.stdin.read()
    grid = [list(line) for line in inp.splitlines()]
    rows = len(grid)
    cols = len(grid[0])
    print(rows, cols)

    # print_grid(grid)

    # find initial position by finding "^"
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == "^":
                pos = (i, j)
                print(f"Initial position: {pos}")
                grid[i][j] = "↑"
                break
    visited, loop = grid_travel(deepcopy(grid), pos, (-1, 0))
    print("part 1:", len(visited))

    # if we record the visited cells, we could do this only on the cells on the taken path
    # obstacles = 0
    # for i, j in visited[1:]:
    #     new_grid = deepcopy(grid)
    #     new_grid[i][j] = "#"
    #     visited, loop = grid_travel(new_grid, pos, (-1, 0))
    #     if loop:
    #         obstacles += 1
    #         # print(f"obstacle at {(i, j)}, visited: {visited}")
    obstacles = grid_travel_2(grid, pos, (-1, 0))
    print(f"part 2: {obstacles}")

    return
    # iterate movement
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dir = (-1, 0)

    def exiting(dir: tuple[int, int], pos: tuple[int, int]):
        i, j = pos
        match dir:
            case (0, 1):
                return j == cols - 1
            case (1, 0):
                return i == rows - 1
            case (0, -1):
                return j == 0
            case (-1, 0):
                return i == 0

    turn_positions = deque()
    obstacles = 0
    while not exiting(dir, pos):
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])
        # print(pos, dir, next_pos)
        # check if we reached the 3rd most recent turn position
        if len(turn_positions) >= 3 and (pos[0] == turn_positions[0][0] or pos[1] == turn_positions[0][1]):
            # if len(turn_positions) >= 2 and (pos[0] == turn_positions[0][0] or pos[1] == turn_positions[0][1]):
            print(f"obstacle at {next_pos}")
            obstacles += 1
        # move
        if grid[next_pos[0]][next_pos[1]] in {".", "X"}:
            # the space is empty, move to it
            pos = next_pos
            # also mark the space as visited
            # grid[pos[0]][pos[1]] = "-" if dir in {(0, 1), (0, -1)} else "|"
            grid[pos[0]][pos[1]] = "X"
        elif grid[next_pos[0]][next_pos[1]] == "#":
            # the space is a wall, change direction
            dir = directions[(directions.index(dir) + 1) % 4]
            # we add the turn position to the deque
            turn_positions.append(pos)

    # we can keep track of the last 3 obstacles that made us turn (using a deque)
    # and every time we reach one of the coordinates of the 3rd most recent obstacle,
    # we increment the obstacles counter

    # now count the number of visited spaces
    visited = 0
    for line in grid:
        for char in line:
            if char in {"X"}:
                visited += 1
    print("part 1:", visited)
    print("part 2:", obstacles)


if __name__ == "__main__":
    main()
