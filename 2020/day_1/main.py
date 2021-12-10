import fileinput
from itertools import product


GOAL = 2020


if __name__ == "__main__":

    amounts = [int(n) for n in fileinput.input()]

    for n1, n2 in product(amounts, repeat=2):
        if n1 + n2 == GOAL:
            print("Part 1", n1, n2, n1 * n2)
            break

    for n1, n2, n3 in product(amounts, repeat=3):
        if n1 + n2 + n3 == GOAL:
            print("Part 2", n1, n2, n3, n1 * n2 * n3)
            break
