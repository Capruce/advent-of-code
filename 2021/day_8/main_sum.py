import fileinput
from typing import Dict, List, Mapping

SEGMENTS = "abcdefg"


def calculate_number_of_occurrences(signals: List[str]) -> Dict[str, int]:
    return {
        segment: sum(1 for signal in signals if segment in signal)
        for segment in SEGMENTS
    }


DIGIT_TO_SEGMENTS: Mapping[int, str] = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}

SEGMENT_TO_NUM_OCCURRENCES = calculate_number_of_occurrences(list(DIGIT_TO_SEGMENTS.values()))

SUM_TO_DIGIT = {
    sigma: digit
    for digit, segments in DIGIT_TO_SEGMENTS.items()
    for sigma in (sum(
        SEGMENT_TO_NUM_OCCURRENCES[segment]
        for segment in segments
    ),)
}


# This is based on the idea that the sum of occurrences for each segment
# used in a digit is unique.
# E.g. segment 'a' is lit in 8 digits, 'c' is lit in 8 digits, and 'f' is lit in
# 9 digits. This means the digit 7 ('a', 'c', 'f') is uniquely represented by
# the sum 8 + 8 + 9 = 25
#
# Since each digit appears exactly once in the scrambled inputs, we can rerun
# the process. We map the number of occurrences of each signal 'a'-'g' across
# all inputs then sum them.
# We know that the input with a sum of 25 must represent the digit 7 and so on.
if __name__ == "__main__":

    scrambled_and_outputs = [
        (scrambled.split(" "), outputs.split(" "))
        for line in fileinput.input()
        for scrambled, outputs in (line.strip().split(" | "),)
    ]

    total = 0
    for signals, outputs in scrambled_and_outputs:
        segment_to_number_of_occurrences = calculate_number_of_occurrences(signals)
        signal_to_digit = {
            frozenset(signal): SUM_TO_DIGIT[sigma]
            for signal in signals
            for sigma in (sum(
                segment_to_number_of_occurrences[segment]
                for segment in signal
            ),)
        }

        total += int("".join(
            str(signal_to_digit[frozenset(output)])
            for output in outputs
        ))

    print("Part 2:", total)

