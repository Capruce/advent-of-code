import fileinput
from functools import reduce
import operator
from typing import Dict, List, Tuple


Point = Tuple[int, int]
Map = Dict[Point, int]


def get_adjacent_points(map_: Map, point: Point) -> List[Point]:
    i, j = point
    return [
        p
        for i_a, j_a in [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
        if (p := (i_a, j_a)) in map_
    ]


def calculate_size_of_basin(map_: Map, local_minima: Point) -> int:
    points_to_visit = [local_minima]
    points_in_basin = set()
    while points_to_visit:
        point = points_to_visit.pop()
        if point in points_in_basin:
            continue
        points_in_basin.add(point)

        for a in get_adjacent_points(map_, point):
            if a not in points_in_basin and map_[a] != 9:
                points_to_visit.append(a)
    return len(points_in_basin)


def load_map() -> Map:
    return {
        (i, j): int(h)
        for i, line in enumerate(fileinput.input())
        for j, h in enumerate(line.strip())
    }


if __name__ == "__main__":
    MAP = load_map()

    minima = [
        p
        for p, h in MAP.items()
        if h < min(MAP[a] for a in get_adjacent_points(MAP, p))
    ]

    part_1 = sum(MAP[p] + 1 for p in minima)
    print("Part 1:", part_1)

    basin_sizes = sorted(map(lambda p: calculate_size_of_basin(MAP, p), minima), reverse=True)
    part_2 = reduce(operator.mul, basin_sizes[:3])
    print("Part 2:", part_2)
