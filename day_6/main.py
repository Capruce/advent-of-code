from collections import Counter, defaultdict
import fileinput
from typing import Dict

NEW_TIME_TO_REPRODUCE    = 8
REPEAT_TIME_TO_REPRODUCE = 6


def simulate(current_state: Dict[int, int], days: int) -> int:
    for day in range(days):
        next_state: Dict[int, int] = defaultdict(int)

        for time_to_reproduce, count in current_state.items():
            if time_to_reproduce == 0:
                next_state[NEW_TIME_TO_REPRODUCE] += count
                next_state[REPEAT_TIME_TO_REPRODUCE] += count
            else:
                next_state[time_to_reproduce - 1] += count

        current_state = next_state

    return sum(current_state.values())


if __name__ == "__main__":
    initial_state = Counter((
        int(time_to_reproduce)
        for line in fileinput.input()
        for time_to_reproduce in line.split(",")
    ))

    print("Part 1:", simulate(initial_state, 80))
    print("Part 2:", simulate(initial_state, 256))
