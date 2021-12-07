import fileinput
from statistics import median, mean
from typing import List


def calculate_linear_fuel_usage(positions: List[int], target: int) -> int:
    return sum(
        abs(target - x_i) * (abs(target - x_i) + 1) // 2
        for x_i in positions
    )


def calculate_constant_fuel_usage(positions: List[int], target: int) -> int:
    return sum(abs(target - n) for n in positions)


if __name__ == "__main__":

    positions = sorted((
        int(n)
        for line in fileinput.input()
        for n in line.split(",")
    ))

    cheapest_position = int(median(positions))
    constant_fuel_usage = calculate_constant_fuel_usage(positions, cheapest_position)
    print("Part 1:", cheapest_position, constant_fuel_usage)

    cheapest_position = int(mean(positions))
    linear_fuel_usage = calculate_linear_fuel_usage(positions, cheapest_position)
    print("Part 2:", cheapest_position, linear_fuel_usage)


