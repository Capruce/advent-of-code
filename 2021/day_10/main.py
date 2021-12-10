import fileinput
from functools import reduce

OPEN  = ["(", "[", "{", "<"]
CLOSE = [")", "]", "}", ">"]
SCORE = [3, 57, 1197, 25137]

if __name__ == "__main__":
    lines = [line.strip() for line in fileinput.input()]

    syntax_error_score = 0
    autocomplete_scores = []
    for line in lines:
        stack = []
        for symbol in line:
            try:
                index = OPEN.index(symbol)
            except ValueError:
                if stack.pop(-1) != (index := CLOSE.index(symbol)):
                    syntax_error_score += SCORE[index]
                    break
            else:
                stack.append(index)
        else:
            autocomplete_scores.append(
                reduce(lambda t, i: (t * 5) + i + 1, reversed(stack), 0)
            )

    print("Part 1:", syntax_error_score)

    autocomplete_scores = sorted(autocomplete_scores)
    middle = autocomplete_scores[len(autocomplete_scores) // 2]
    print("Part 2:", middle)
