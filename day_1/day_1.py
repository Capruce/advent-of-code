from typing import Iterable, Tuple


def count_increases(s: Iterable[Tuple[int, int]]) -> int:
    total = 0
    for left, right in s:
        if right > left:
            total += 1
    return total


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        readings = [int(l) for l in f.readlines()]

    print(count_increases(zip(readings[:-1], readings[1:])))

    sums = list(map(sum, zip(readings[:-2], readings[1:-1], readings[2:])))
    print(count_increases(zip(sums[:-1], sums[1:])))

