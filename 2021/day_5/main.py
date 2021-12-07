from collections import defaultdict
from dataclasses import dataclass
import fileinput
from typing import DefaultDict, Iterator, List, Tuple


def birange(start_inc: int, stop_inc: int) -> List[int]:
    if start_inc <= stop_inc:
        return list(range(start_inc, stop_inc + 1))
    return list(range(start_inc, stop_inc - 1, -1))


@dataclass(frozen=True)
class Vent:
    start: Tuple[int, int]
    stop: Tuple[int, int]

    def __str__(self) -> str:
        return f"{self.start} -> {self.stop}"

    @classmethod
    def from_raw(cls, raw: str) -> "Vent":
        start, stop = (
            (int(x), int(y))
            for point in raw.split(" -> ")
            for x, y in (point.split(","),)
        )
        return Vent(start, stop)

    def is_horizontal(self) -> bool:
        return self.start[0] == self.stop[0]

    def is_vertical(self) -> bool:
        return self.start[1] == self.stop[1]

    def coords(self) -> Iterator[Tuple[int, int]]:
        x_values = birange(self.start[0], self.stop[0])
        y_values = birange(self.start[1], self.stop[1])

        if len(x_values) == 1:
            x_values = x_values * len(y_values)
        elif len(y_values) == 1:
            y_values = y_values * len(x_values)

        return (p for p in zip(x_values, y_values))


class Map:
    coord_to_number_of_vents: DefaultDict[Tuple[int, int], int]

    def __init__(self) -> None:
        self.coord_to_number_of_vents = defaultdict(int)

    def map_vents(self, vents: List[Vent]) -> None:
        for vent in vents:
            for x, y in vent.coords():
                self.coord_to_number_of_vents[(x, y)] += 1

    def count_coords_gte(self, n: int) -> int:
        return sum(
            1
            for count in self.coord_to_number_of_vents.values()
            if count >= n
        )


if __name__ == "__main__":
    all_vents = [
        Vent.from_raw(row)
        for row in fileinput.input()
    ]

    h_and_v_vents = []
    diagonal_vents = []
    for vent in all_vents:
        if vent.is_horizontal() or vent.is_vertical():
            h_and_v_vents.append(vent)
        else:
            diagonal_vents.append(vent)

    sea_floor = Map()
    sea_floor.map_vents(h_and_v_vents)
    print("Part 1:", sea_floor.count_coords_gte(2))

    sea_floor.map_vents(diagonal_vents)
    print("Part 2:", sea_floor.count_coords_gte(2))
