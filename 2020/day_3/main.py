from dataclasses import dataclass
import fileinput
from functools import reduce
import operator
from typing import Dict, Iterator, Tuple


@dataclass
class Layout:
    layout: Dict[Tuple[int, int], bool]
    width: int
    height: int

    @classmethod
    def from_raw(cls, raw: Iterator[str]) -> "Layout":
        layout = {
            (x, y): symbol == "#"
            for y, line in enumerate(raw)
            for x, symbol in enumerate(line.strip())
        }
        width = max(x for x, _ in layout.keys()) + 1
        height = max(y for _, y in layout.keys()) + 1

        return Layout(layout, width, height)

    def calc_trees_hit(self, delta_x: int, delta_y: int) -> int:
        x = 0
        y = 0
        trees_hit = 0
        while y < self.height:
            if self.layout[(x, y)]:
                trees_hit += 1

            x = (x + delta_x) % self.width
            y += delta_y

        return trees_hit


if __name__ == "__main__":

    layout = Layout.from_raw(fileinput.input())

    print("Part 1:", layout.calc_trees_hit(3, 1))

    SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    part_2 = reduce(
        operator.mul,
        (layout.calc_trees_hit(x, y) for x, y in SLOPES)
    )
    print("Part 2:", part_2)
