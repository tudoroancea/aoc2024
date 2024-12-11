from aoc2024.utils import sys, deepcopy


def part1(disk_layout: list[str]):
    reordered_disk_layout = deepcopy(disk_layout)
    # reorder disk
    i, j = 0, len(reordered_disk_layout) - 1
    # input()
    while i < j:
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

    # compute checksum
    print("part 1: ", sum(i * int(n) for i, n in enumerate(reordered_disk_layout) if n != "."))


def part2(disk_layout: list[str], file_blocks: list[tuple[int, int]], empty_blocks: list[tuple[int, int]]):
    reordered_disk_layout = deepcopy(disk_layout)
    # for each file block, we check all the empty blocks to its left, and move
    # the file to the leftmost empty block in which it fits (if there is one),
    # otherwise we skip it
    for file_start, file_end in file_blocks[::-1]:
        for i, (empty_block_start, empty_block_end) in enumerate(empty_blocks):
            if empty_block_start >= file_end:
                # we don't move the file
                break
            if empty_block_end - empty_block_start >= file_end - file_start:
                # the file fits, so we move it
                reordered_disk_layout[empty_block_start : empty_block_start + file_end - file_start] = reordered_disk_layout[file_start:file_end]
                reordered_disk_layout[file_start:file_end] = ["."] * (file_end - file_start)
                # update the empty block size
                empty_blocks[i] = (empty_block_start + (file_end - file_start), empty_block_end)
                break

    print("".join(reordered_disk_layout))
    print("part 2: ", sum(i * int(n) for i, n in enumerate(reordered_disk_layout) if n != "."))


def main():
    disk_map = list(sys.stdin.read().strip())
    # with open("data/9.txt", "r") as f:
    #     disk_map = list(f.readline().strip())

    # crate initial disk layout
    disk_layout: list[str] = []
    file_blocks: list[tuple[int, int]] = []  # immutable
    empty_blocks: list[tuple[int, int]] = []  # when me move a file to an empty block, we override the range of the empty block
    file_id = 0
    for i in range(0, len(disk_map), 2):
        # append a file block
        file_blocks.append((len(disk_layout), len(disk_layout) + int(disk_map[i])))
        disk_layout += [str(file_id)] * int(disk_map[i])

        file_id += 1

        if i + 1 < len(disk_map):
            # append an empty block
            empty_blocks.append((len(disk_layout), len(disk_layout) + int(disk_map[i + 1])))
            disk_layout += ["."] * int(disk_map[i + 1])

    part1(disk_layout)
    part2(disk_layout, file_blocks, empty_blocks)


if __name__ == "__main__":
    main()
