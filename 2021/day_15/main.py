import fileinput
from queue import PriorityQueue
from typing import Dict, List, Tuple

Point = Tuple[int, int]
Map = Dict[Point, int]


def load_map() -> Map:
    return {
        (int(x), int(y)): int(cost)
        for y, row in enumerate(fileinput.input())
        for x, cost in enumerate(row.strip())
    }


def neighbours(map_: Map, point: Point) -> List[Point]:
    i, j = point
    return [
        neighbour
        for neighbour in [
                        (i, j - 1),
            (i - 1, j),             (i + 1, j),
                        (i, j + 1),
        ]
        if neighbour in map_
    ]


def cheapest_path(map_: Map, start: Point, target: Point) -> int:
    if start == target:
        return 0

    # (f, (x, y), g)
    open_set = PriorityQueue()
    open_set.put((map_[start], start, 0))

    closed_set = {}

    while open_set:
        c_f, c_p, c_g = open_set.get()

        if c_p in closed_set and c_f >= closed_set[c_p]:
            continue

        for n_p in neighbours(map_, c_p):
            n_g = c_g + map_[n_p]

            if n_p == target:
                return n_g

            n_h = (target[0] - n_p[0]) + (target[1] - n_p[1])
            n_f = n_g + n_h

            if n_p in closed_set and (n_f >= closed_set[n_p]):
                continue

            open_set.put((n_f, n_p, n_g))

        closed_set[c_p] = c_f

    raise AssertionError("No path to target.")


def expand_x(map_: Map) -> Map:
    width = sorted(map_.keys())[-1][0] + 1
    return {
        (x + (width * n), y): p - 9 if (p := v + n) > 9 else p
        for (x, y), v in map_.items()
        for n in range(5)
    }


def expand_y(map_: Map) -> Map:
    height = sorted(map_.keys())[-1][1] + 1
    return {
        (x, y + (height * n)): p - 9 if (p := v + n) > 9 else p
        for (x, y), v in map_.items()
        for n in range(5)
    }


def expand_map(map_: Map) -> Map:
    return expand_y(expand_x(map_))


if __name__ == "__main__":
    MAP = load_map()

    START = (0, 0)
    END = sorted(MAP.keys())[-1]
    print("Part 1:", cheapest_path(MAP, START, END))

    EXPANDED = expand_map(MAP)
    END = sorted(EXPANDED.keys())[-1]
    print("Part 2:", cheapest_path(EXPANDED, START, END))
