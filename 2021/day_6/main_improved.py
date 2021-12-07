import fileinput
from typing import List


NEW_TIME_TO_REPRODUCE    = 8
REPEAT_TIME_TO_REPRODUCE = 6


def simulate(current_state: List[int], days: int) -> int:
    state = current_state.copy()  # Shallow copy
    for _ in range(days):
        number_reproducing = state.pop(0)
        state[REPEAT_TIME_TO_REPRODUCE] += number_reproducing
        state[NEW_TIME_TO_REPRODUCE] += number_reproducing

    return sum(state)


if __name__ == "__main__":
    times_to_reproduce = [
        int(n)
        for line in fileinput.input()
        for n in line.split()
    ]
    initial_state = [
        times_to_reproduce.count(n)
        for n in range(NEW_TIME_TO_REPRODUCE + 1)
    ]

    print("Part 1:", simulate(initial_state, 80))
    print("Part 2:", simulate(initial_state, 256))
