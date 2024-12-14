from typing import Optional
from aoc2024.utils import sys, timeit, re, np
import scipy

np.set_printoptions(linewidth=420, threshold=10000000000)


def main():
    # inp = sys.stdin.read()
    with open("data/14.txt", "r") as f:
        inp = f.read()
    matches = re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", inp)
    x_max, y_max = 101, 103

    grid = np.zeros((x_max, y_max), dtype=int)
    guards_x = []
    guards_y = []
    guards_vx = []
    guards_vy = []
    for match in matches:
        x, y, vx, vy = int(match[0]), int(match[1]), int(match[2]), int(match[3])
        guards_x.append(x)
        guards_y.append(y)
        guards_vx.append(vx)
        guards_vy.append(vy)
        x_final, y_final = (x + 100 * vx) % x_max, (y + 100 * vy) % y_max
        grid[x_final, y_final] += 1
    print(
        "part 1:",
        np.sum(grid[: x_max // 2, : y_max // 2])
        * np.sum(grid[: x_max // 2, y_max // 2 + 1 :])
        * np.sum(grid[x_max // 2 + 1 :, : y_max // 2])
        * np.sum(grid[x_max // 2 + 1 :, y_max // 2 + 1 :]),
    )
    bruh = [
        list(map(int, list(line)))
        for line in """000000000010000000000
000000000111000000000
000000001111100000000
000000011111110000000
000000111111111000000
000000001111100000000
000000011111110000000
000000111111111000000
000001111111111100000
000011111111111110000
000000111111111000000
000001111111111100000
000011111111111110000
000111111111111111000
001111111111111111100
000011111111111110000
000111111111111111000
001111111111111111100
011111111111111111110
111111111111111111111
000000000111000000000
000000000111000000000
000000000111000000000
""".splitlines()
    ]
    tree = np.array(bruh).astype(np.int64).T
    guards_x = np.array(guards_x)
    guards_y = np.array(guards_y)
    guards_vx = np.array(guards_vx)
    guards_vy = np.array(guards_vy)
    found: Optional[int] = None
    counter = 0
    batch_size = 1000
    while found is None:
        grid = np.zeros((x_max, y_max, batch_size), dtype=np.int64)  # X,Y,B
        batch_id = np.arange(counter * batch_size, (counter + 1) * batch_size)  # B
        x_idx = np.remainder((guards_x[None, :] + guards_vx[None, :] * batch_id[:, None]), x_max).ravel()  # G,B
        y_idx = np.remainder((guards_y[None, :] + guards_vy[None, :] * batch_id[:, None]), y_max).ravel()  # G,B
        z_idx = np.repeat(np.arange(batch_size), guards_x.size)
        grid[x_idx, y_idx, z_idx] = 1
        corr = scipy.ndimage.correlate(grid, tree[:, :, None], mode="constant")
        if np.any(corr == np.sum(tree)):
            found = batch_id[np.argwhere(corr == np.sum(tree))[0][2]]
        counter += 1
    print("part 2:", found)


if __name__ == "__main__":
    main()
