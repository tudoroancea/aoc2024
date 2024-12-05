from collections import defaultdict, deque
from functools import partial

from aoc2024.utils import sys, timeit


def check_rules(dag: dict[int, set[int]], seq: list[int]):
    # Track the positions of elements in the sequence
    positions = {elem: idx for idx, elem in enumerate(seq)}

    # Check that each element comes before the successors
    for node, successors in dag.items():
        # If the node is in the sequence
        if node in positions:
            # Check that all dependencies appear earlier in the sequence
            for suc in successors:
                if suc in positions and positions[suc] <= positions[node]:
                    return False

    return True


def topo_sort(dag: dict[int, set[int]], nodes: list[int]) -> list[int]:
    """
    Perform a topological sort on a given set of nodes respecting the partial order.

    Args:
    - dag: A dictionary representing the directed acyclic graph of order relations
           Keys are nodes, values are sets of nodes that must come after the key
    - nodes: List of nodes to be sorted

    Returns:
    - A topologically sorted list of nodes, or None if no valid sorting exists
    """
    # Isolate the part of the DAG based on the relevant nodes
    in_degree = defaultdict(int)
    graph = defaultdict(set)
    for source, destinations in dag.items():
        if source in nodes:
            for dest in destinations:
                if dest in nodes:
                    if dest not in graph[source]:
                        graph[source].add(dest)
                        in_degree[dest] += 1

    # Initialize queue with nodes having no incoming edges
    queue = deque([node for node in nodes if in_degree[node] == 0])

    # Result list to store sorted order
    sorted_nodes = []

    # Perform topological sorting
    while queue:
        # Remove a node with no incoming edges
        current = queue.popleft()
        sorted_nodes.append(current)

        # Reduce in-degree for adjacent nodes
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            # If in-degree becomes 0, add to queue
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check if all nodes are sorted (detect cycles or unsortable nodes)
    if len(sorted_nodes) != len(nodes):
        return None  # Impossible to totally order

    return sorted_nodes


@timeit
def part1(rules: list[tuple[int, int]], updates: list[list[int]]):
    # create DAG to represent the rules
    dag = defaultdict(set)
    for rule in rules:
        dag[rule[0]].add(rule[1])
    # find the sum of the middle element of each valid update
    print("part 1:", sum(update[len(update) // 2] for update in updates if check_rules(dag, update)))


@timeit
def part2(rules: list[tuple[int, int]], updates: list[list[int]]):
    # create DAG to represent the rules
    dag = defaultdict(set)
    for rule in rules:
        dag[rule[0]].add(rule[1])
    # find invalid updates and sort them
    sorted_updates = list(map(partial(topo_sort, dag), filter(lambda u: not check_rules(dag, u), updates)))
    # find the sum of the middle element of each sorted update
    print("part 2:", sum(sorted_update[len(sorted_update) // 2] for sorted_update in sorted_updates))


def main():
    inp = sys.stdin.read()
    lines = inp.splitlines()
    sep = lines.index("")
    rules = [(int(line[:2]), int(line[3:])) for line in lines[:sep]]
    updates = [list(map(lambda s: int(s), line.split(","))) for line in lines[sep + 1 :]]
    part1(rules, updates)
    part2(rules, updates)


if __name__ == "__main__":
    main()
