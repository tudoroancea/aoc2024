from aoc2024.utils import sys, timeit


def concat(x: int, y: int):
    return x * pow(10, len(str(y))) + y


def validate_equation(expected_result: int, first_operand: int, other_operands: list[int], part2: bool = False, verbose=False) -> bool:
    if verbose:
        print(f"validating {first_operand} {other_operands} with {expected_result}")
    # between each pair of consecutive operands, we can add either * or +.
    # this basically amounts to a binary tree of possible sequence of operations
    # with depth len(numbers) - 1.
    # While traversing it, if at some point we have a temporary result that is
    # bigger than the expected result, we can discard the whole sub tree.
    if len(other_operands) == 1:
        if first_operand * other_operands[0] == expected_result:
            if verbose:
                print("validated")
            return True
        if first_operand + other_operands[0] == expected_result:
            if verbose:
                print("validated")
            return True
        if part2 and concat(first_operand, other_operands[0]) == expected_result:
            if verbose:
                print("validated")
            return True
        return False
    else:
        if first_operand * other_operands[0] <= expected_result and validate_equation(
            expected_result, first_operand * other_operands[0], other_operands[1:], part2
        ):
            return True
        if first_operand + other_operands[0] <= expected_result and validate_equation(
            expected_result, first_operand + other_operands[0], other_operands[1:], part2
        ):
            return True
        if (
            part2
            and concat(first_operand, other_operands[0]) <= expected_result
            and validate_equation(expected_result, concat(first_operand, other_operands[0]), other_operands[1:], part2)
        ):
            return True
        return False


@timeit
def part1(equations: list[tuple[int, list[int]]]):
    print(
        "part 1: ",
        sum(expected_result for expected_result, operands in equations if validate_equation(expected_result, operands[0], operands[1:], False)),
    )


@timeit
def part2(equations: list[tuple[int, list[int]]]):
    print(
        "part 2: ",
        sum(expected_result for expected_result, operands in equations if validate_equation(expected_result, operands[0], operands[1:], True)),
    )


def main():
    inp = sys.stdin.read()
    lines = inp.splitlines()
    equations = []
    for line in lines:
        i = line.find(":")
        equations.append((int(line[:i]), list(map(int, line[i + 1 :].split(" ")[1:]))))
    part1(equations)
    part2(equations)


if __name__ == "__main__":
    main()
