import fileinput
from functools import reduce
from typing import List, Literal, Set, Tuple


Point = Tuple[int, int]
Paper = Set[Point]
FoldInst = Tuple[Literal["x", "y"], int]


def load() -> Tuple[Paper, List[FoldInst]]:
    raw = "".join(fileinput.input()).strip()

    raw_coords, raw_instructions = raw.split("\n\n")

    paper = set(
        (int(x), int(y))
        for point in raw_coords.split("\n")
        for x, y in (point.strip().split(","),)
    )

    instructions = [
        (axis, int(amount))
        for inst in raw_instructions.split("\n")
        for axis, amount in (inst.strip()[11:].split("="),)
    ]

    return paper, instructions


def print_paper(paper: Paper) -> None:
    width  = max(p[0] for p in paper)
    height = max(p[1] for p in paper)

    print("\n".join(
        "".join(
            " #" if (x, y) in paper else " ."
            for x in range(width)
        )
        for y in range(height)
    ))


def fold(paper: Paper, instruction: FoldInst) -> Paper:
    axis, value = instruction
    if axis == "y":
        return set((x, value - abs(value - y)) for x, y in paper)
    return set((value - abs(value - x), y) for x, y in paper)


if __name__ == "__main__":
    PAPER, INSTRUCTIONS = load()

    print("Part 1:", len(fold(PAPER, INSTRUCTIONS[0])))
    print("Part 2:")
    print_paper(reduce(fold, INSTRUCTIONS, PAPER))

