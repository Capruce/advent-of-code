from collections import defaultdict
import fileinput
from functools import reduce
import operator
from typing import Dict, Optional, Set, Tuple

Graph = Dict[str, Set[str]]
Cave = str
Path = Tuple[Cave, ...]

START = "start"
END = "end"


def load_graph() -> Graph:
    graph = defaultdict(set)
    for line in fileinput.input():
        left, right = line.strip().split("-")
        graph[left].add(right)
        graph[right].add(left)
    return dict(graph)


def is_small(cave: Cave) -> bool:
    return cave.islower()


def find_paths(
    graph: Graph,
    path_so_far: Path,
    can_visit_twice: Optional[Cave] = None,
) -> Set[Path]:
    paths = set()
    for cave in graph[path_so_far[-1]]:
        path = (*path_so_far, cave)
        if cave == END:
            paths.add(path)
        elif not is_small(cave):
            paths.update(find_paths(graph, path, can_visit_twice))
        elif cave == can_visit_twice and path_so_far.count(cave) < 2:
            paths.update(find_paths(graph, path, can_visit_twice))
        elif cave not in path_so_far:
            paths.update(find_paths(graph, path, can_visit_twice))
    return paths


def find_number_of_paths(graph: Graph) -> int:
    return len(find_paths(graph, (START,)))


def find_number_of_paths_2(graph: Graph) -> int:
    return len(reduce(
        operator.or_, (
            find_paths(graph, (START,), cave)
            for cave in graph.keys()
            if is_small(cave) and cave not in [START, END]
        )
    ))


if __name__ == "__main__":
    GRAPH = load_graph()

    print("Part 1:", find_number_of_paths(GRAPH))
    print("Part 2:", find_number_of_paths_2(GRAPH))
