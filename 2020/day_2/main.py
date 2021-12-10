import fileinput
import re

RE = re.compile("(\d+)-(\d+) ([a-z]): (.+)")

if __name__ == "__main__":

    inputs = [
        (int(low), int(high), letter, password)
        for line in fileinput.input()
        for low, high, letter, password in (RE.match(line).groups(),)
    ]

    part_1 = sum(
        1
        for low, high, letter, password in inputs
        if low <= password.count(letter) <= high
    )
    print("Part 1:", part_1)

    part_2 = sum(
        1
        for low, high, letter, password in inputs
        if (password[low - 1] == letter) != (password[high - 1] == letter)
    )
    print("Part 2:", part_2)


