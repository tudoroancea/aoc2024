from aoc2024.utils import cache


def main():
    # with open("data/19.txt") as f:
    with open("data/19.txt") as f:
        lines = f.read().splitlines()
    patterns = lines[0].split(", ")
    designs = lines[2:]

    @cache
    def is_design_feasible(design: str) -> bool:
        if design in patterns:
            return True
        for pattern in patterns:
            if design.startswith(pattern) and is_design_feasible(design[len(pattern) :]):
                return True
        return False

    def is_design_feasible2(design: str) -> bool:
        n = len(design)
        dp = [False] * (n + 1)
        dp[n] = True
        for i in range(n - 1, -1, -1):
            for pattern in patterns:
                if design[i:].startswith(pattern) and i + len(pattern) <= n and dp[i + len(pattern)]:
                    dp[i] = True
                    break
        return dp[0]

    print("part 1:", sum(is_design_feasible2(design) for design in designs))

    @cache
    def feasibility_index(design: str) -> int:
        # greedy algorithm
        n = 1 if design in patterns else 0
        for pattern in patterns:
            if design.startswith(pattern):
                n += feasibility_index(design[len(pattern) :])
        return n

    print("part 2:", sum(feasibility_index(design) for design in designs))


if __name__ == "__main__":
    main()
