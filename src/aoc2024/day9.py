from copy import deepcopy
from aoc2024.utils import sys


def main():
    disk_map = list(sys.stdin.read().strip())
    print("".join(disk_map))
    size = len(disk_map)

    # crate initial disk layout
    initial_disk_layout = ""
    file_id = 0
    for i in range(0, len(disk_map), 2):
        initial_disk_layout += str(file_id) * int(disk_map[i])
        file_id += 1
        if i + 1 < len(disk_map):
            initial_disk_layout += "." * int(disk_map[i + 1])
    initial_disk_layout = list(initial_disk_layout)
    # reorder disk
    i, j = 0, len(initial_disk_layout) - 1
    reordered_disk_layout = deepcopy(initial_disk_layout)
    if size <= 100:
        print(f"i={i:4d}, j={j:4d}, -> {''.join(reordered_disk_layout)}")
    while i < j:
        # if reordered_disk_layout[i] == "." and reordered_disk_layout[j] != ".":
        #     # we swap
        #     reordered_disk_layout[i], reordered_disk_layout[j] = reordered_disk_layout[j], reordered_disk_layout[i]
        #     i += 1
        #     j -= 1
        # else:
        #     if reordered_disk_layout[j] == ".":
        #         # we don't haven anything to move from the right
        #         j -= 1
        #     if reordered_disk_layout[i] != ".":
        #         # the left position is not empty, so we advance it
        #         i += 1

        # Find the next empty space from the left
        while i < j and reordered_disk_layout[i] != ".":
            i += 1
        # Find the next file block from the right
        while i < j and reordered_disk_layout[j] == ".":
            j -= 1
        # If we found both an empty space and a file block, swap them
        if i < j:
            reordered_disk_layout[i], reordered_disk_layout[j] = reordered_disk_layout[j], reordered_disk_layout[i]
            i += 1
            j -= 1

        if size <= 100:
            print(f"i={i:4d}, j={j:4d}, -> {''.join(reordered_disk_layout)}")
    reordered_disk_layout = "".join(reordered_disk_layout)

    # check that after the first ".", there are no more numbers
    # assert reordered_disk_layout == "0099811188827773336446555566.............."
    assert (first_dot := reordered_disk_layout.find(".")) == -1 or set(reordered_disk_layout[first_dot + 1 :]) == {"."}
    # compute checksum
    print("part 1: ", sum(i * int(n) for i, n in enumerate(reordered_disk_layout[:first_dot])))


if __name__ == "__main__":
    main()
