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


def grid_travel(grid: list[list[str]], pos: tuple[int, int], dir: tuple[int, int], verbose: bool = False) -> tuple[list[tuple[int, int]], bool]:
    """
    We wander through the grid starting from a given position pos and with direction
    dir, until we exit the grid or encounter a loop. While traveling, we mark the
    visited cells in the grid using "↑", "→", "↓", "←" and return the list of visited
    cells. We also check if we are in a loop, and return True if we are.

    Args:
        grid (list[list[str]]): The grid to travel through.
        pos (tuple[int, int]): The starting position.
        dir (tuple[int, int]): The direction to travel.

    Returns:
        tuple[list[tuple[int, int]], bool]: A tuple containing the list of visited cells
            and a boolean indicating if we are in a loop.
    """
    if verbose:
        print(f"Starting at {pos}")
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    directions_char = ["↑", "→", "↓", "←"]
    visited = [pos]
    while not (
        (dir == (0, 1) and pos[1] == cols - 1)
        or (dir == (1, 0) and pos[0] == rows - 1)
        or (dir == (0, -1) and pos[1] == 0)
        or (dir == (-1, 0) and pos[0] == 0)
    ):
        if grid[pos[0]][pos[1]] == directions_char[directions.index(dir)]:
            # we were already here and took the same direction,
            # so we are in a loop
            if verbose:
                print_grid(grid)
            return visited, True
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if verbose:
            print(f"next pos: {next_pos}")
        if grid[next_pos[0]][next_pos[1]] in ["."] + directions_char:
            if grid[next_pos[0]][next_pos[1]] == ".":
                # count next_pos as visited
                if verbose:
                    print(f"visiting {next_pos}")
                visited.append(next_pos)
            # mark direction taken at current cell
            grid[pos[0]][pos[1]] = directions_char[directions.index(dir)]
            # update pos
            pos = next_pos
        elif grid[next_pos[0]][next_pos[1]] == "#":
            # we are facing an obstacle, so we change direction
            dir = directions[(directions.index(dir) + 1) % 4]
    # mark direction taken at last visited cell
    grid[pos[0]][pos[1]] = directions_char[directions.index(dir)]
    # we made it to the end
    if verbose:
        print_grid(grid)
    return visited, False


def grid_travel_2(grid: list[list[str]], pos: tuple[int, int], dir: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Here we wander around and at each step, if the next pos is free, we try adding an obstacle
    and check if this introduces a loop.
    """
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    directions_char = ["↑", "→", "↓", "←"]
    visited_number = 0
    obstacles = []
    while not (
        (dir == (0, 1) and pos[1] == cols - 1)
        or (dir == (1, 0) and pos[0] == rows - 1)
        or (dir == (0, -1) and pos[1] == 0)
        or (dir == (-1, 0) and pos[0] == 0)
    ):
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if grid[next_pos[0]][next_pos[1]] in ["."] + directions_char:
            if grid[next_pos[0]][next_pos[1]] == ".":
                # the next pos is free, so we check if adding an obstacle
                # introduces a loop
                new_grid = deepcopy(grid)
                new_grid[next_pos[0]][next_pos[1]] = "#"
                # print(f"Adding obstacle at iter {visited_number}")
                _, loop = grid_travel(new_grid, pos, dir)
                visited_number += 1
                if loop:
                    obstacles.append(next_pos)
            # mark direction taken at current cell
            grid[pos[0]][pos[1]] = directions_char[directions.index(dir)]
            # update pos
            pos = next_pos
        elif grid[next_pos[0]][next_pos[1]] == "#":
            # the space is a wall, change direction
            dir = directions[(directions.index(dir) + 1) % 4]
    # mark direction taken at last visited cell
    grid[pos[0]][pos[1]] = directions_char[directions.index(dir)]
    # we made it to the end
    return obstacles


def main():
    inp = sys.stdin.read()
    grid = [list(line) for line in inp.splitlines()]
    rows = len(grid)
    cols = len(grid[0])
    print(f"rows: {rows}, cols: {cols}")
    # find initial position by finding "^"
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == "^":
                pos = (i, j)
                print(f"Initial position: {pos}")
                grid[i][j] = "."
                break
    visited, loop = grid_travel(deepcopy(grid), pos, (-1, 0))
    print("part 1:", len(visited))
    if loop:
        print("LOOP")
        return
    # if we record the visited cells, we could do this only on the cells on the taken path
    obstacles = grid_travel_2(grid, pos, (-1, 0))
    print(f"part 2: {len(obstacles)}")

    return


if __name__ == "__main__":
    main()
