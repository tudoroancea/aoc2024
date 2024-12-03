import sys

import numpy as np


def parse_input(inp: str) -> list[list[int]]:
    lines = inp.splitlines()
    return [[int(el) for el in els] for els in [line.split() for line in lines]]


def main():
    inp = sys.stdin.read()
    reports = parse_input(inp)
    # A report can be tolerated if we can make it safe by remove ONE level.
    # Therefore there can be only two problems that are consecutive
    safe = 0
    for report in reports:
        diff = np.diff(report)
        decreasing = diff < 0
        increasing = diff > 0
        non_increasing = ~increasing
        non_decreasing = ~decreasing
        diff_abs = np.abs(diff)
        small_jumps = diff_abs <= 3
        big_jumps = diff_abs > 3

        idx_max = len(report) - 2  # == len(diff) - 1
        if len(report) <= 2:
            # special case
            safe += 1
        elif np.all(small_jumps) and (np.all(decreasing) or np.all(increasing)):
            # normally safe
            safe += 1
        elif (
            (np.all(decreasing) or np.all(increasing))
            and np.sum(big_jumps) == 1
            and np.argwhere(big_jumps)[0, 0] in {0, idx_max}
        ):
            # sequence is stricly monotonic but there is a unique big jump
            # at either the beginning or the end
            safe += 1
        elif len(report) == 3:
            if np.abs(report[2] - report[0]) <= 3:
                # we can remove the one in the middle
                safe += 1
            else:
                print("report ", report, " is not safe (len 3)")
                continue
        elif np.sum(non_increasing) == 1:
            x = np.argwhere(non_increasing)[0, 0]
            if x == 0:
                # we remove x
                if np.all(diff_abs[:x] <= 3) and np.all(diff_abs[x + 1 :] <= 3):
                    safe += 1
                else:
                    print("report ", report, " is not safe A a")
                    continue
            elif x == idx_max:
                # we remove x+2
                if np.all(diff_abs[: x + 1] <= 3) and np.all(diff_abs[x + 2 :] <= 3):
                    safe += 1
                else:
                    print("report ", report, " is not safe A b")
                    continue
            else:
                # we remove x+1
                if (
                    report[x] < report[x + 2] <= report[x] + 3
                    and np.all(diff_abs[:x] <= 3)
                    and np.all(diff_abs[x + 2 :] <= 3)
                ):
                    safe += 1
                else:
                    print("report ", report, " is not safe A a")
                    continue
        elif np.sum(non_decreasing) == 1:
            x = np.argwhere(non_decreasing)[0, 0]
            # 2 3 4 2 5 is safe (we remove 2 -> x+1)
            # 6 5 4 6 3 is safe (we remove 1 -> x+1)
            if x == 0:
                # we remove x
                if np.all(diff_abs[:x] <= 3) and np.all(diff_abs[x + 1 :] <= 3):
                    safe += 1
                else:
                    print("report ", report, " is not safe B a")
                    continue
            elif x == idx_max:
                # we remove x+2
                if np.all(diff_abs[: x + 1] <= 3) and np.all(diff_abs[x + 2 :] <= 3):
                    safe += 1
                else:
                    print("report ", report, " is not safe B b")
                    continue
            else:
                # we remove x+1
                if (
                    report[x] > report[x + 2] >= report[x] + 3
                    and np.all(diff_abs[:x] <= 3)
                    and np.all(diff_abs[x + 2 :] <= 3)
                ):
                    safe += 1
                else:
                    print("report ", report, " is not safe B c")
                    continue
        else:
            print("report ", report, " is not safe")

    print(safe)


# [4, 2, 5] is safe ; when the sequence is supposed to be increasing, we should remove  x
# [4, 2, 6] is safe ; when the sequence is supposed to be decreasing

if __name__ == "__main__":
    main()
