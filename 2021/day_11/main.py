import fileinput
from functools import reduce
from itertools import count, product
from operator import add
from typing import Dict, List, Tuple


Point = Tuple[int, int]
Map = Dict[Point, int]
FLASH_THRESHOLD = 9


def load_map() -> Map:
    return {
        (i, j): int(charge)
        for i, line in enumerate(fileinput.input())
        for j, charge in enumerate(line.strip())
    }


def adjacent_points(map_: Map, point: Point) -> List[Point]:
    i, j = point
    return [
        p for p in [
            (i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
            (i,     j - 1),             (i,     j + 1),
            (i + 1, j - 1), (i + 1, j), (i + 1, j + 1),
        ]
        if p in map_
    ]


def simulate_step(map_: Map) -> int:
    have_flashed = set()
    points_to_visit = []

    h, w = list(map_.keys())[-1]
    for p in product(range(h + 1), range(w + 1)):
        map_[p] += 1
        if map_[p] > FLASH_THRESHOLD:
            points_to_visit.append(p)

    while points_to_visit:
        p = points_to_visit.pop(0)
        if p in have_flashed:
            continue

        have_flashed.add(p)
        for a in adjacent_points(map_, p):
            map_[a] += 1
            if map_[a] > FLASH_THRESHOLD and a not in have_flashed:
                points_to_visit.append(a)

    for p in have_flashed:
        map_[p] = 0

    return len(have_flashed)


def simulate_steps(map_: Map, steps: int) -> int:
    return reduce(add, (simulate_step(map_) for _ in range(steps)))


def when_do_all_flash(map_: Map) -> int:
    for n in count(1):
        if simulate_step(map_) == len(map_):
            return n
    raise AssertionError("Unreachable.")


if __name__ == "__main__":
    MAP = load_map()
    print("Part 1:", simulate_steps(MAP.copy(), 100))
    print("Part 2:", when_do_all_flash(MAP.copy()))
