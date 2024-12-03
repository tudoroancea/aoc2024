import sys


def parse_input(inp: str) -> list[tuple[int, int]]:
    lines = inp.splitlines()
    return [(int(x), int(y)) for x, y in [line.split() for line in lines]]


def main():
    inp = sys.stdin.read()
    numbers = parse_input(inp)
    list1 = [line[0] for line in numbers]
    list2 = [line[1] for line in numbers]

    m = max(max(list1), max(list2))

    occurences = {n: 0 for n in range(m + 1)}
    for n in list2:
        occurences[n] += 1

    similarity = sum(n * occurences[n] for n in list1)
    print(similarity)


if __name__ == "__main__":
    main()
