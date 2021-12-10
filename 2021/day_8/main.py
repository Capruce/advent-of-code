import fileinput
from functools import reduce
import operator
from typing import AbstractSet, Dict, List, Mapping, Set

ALL_LETTERS = "abcdefg"


DIGIT_TO_SEGMENTS: Mapping[int, AbstractSet[str]] = {
    0: {"a", "b", "c", "e", "f", "g"},
    1: {"c", "f"},
    2: {"a", "c", "d", "e", "g"},
    3: {"a", "c", "d", "f", "g"},
    4: {"b", "c", "d", "f"},
    5: {"a", "b", "d", "f", "g"},
    6: {"a", "b", "d", "e", "f", "g"},
    7: {"a", "c", "f"},
    8: {"a", "b", "c", "d", "e", "f", "g"},
    9: {"a", "b", "c", "d", "f", "g"},
}

DIGIT_TO_LENGTH = {
    k: len(v)
    for k, v in DIGIT_TO_SEGMENTS.items()
}

LENGTH_TO_COMMON_SEGMENTS = {
    2: {"c", "f"},
    3: {"a", "c", "f"},
    4: {"b", "c", "d", "f"},
    5: {"a", "d", "g"},
    6: {"a", "b", "f", "g"},
    7: {"a", "b", "c", "d", "e", "f", "g"},
}

# Length 5
# 2 | a cde g
# 3 | a cd fg
# 5 | ab d fg
#     a  d  g  are common
#      bc  f   are not

# Length 6
# 0 | abc efg
# 6 | ab defg
# 9 | abcd fg
#     ab   fg are common
#       cde   are not


def get_possible_numbers(signal: str) -> List[int]:
    return [
        number
        for number, segments in DIGIT_TO_SEGMENTS.items()
        if len(signal) == len(segments)
    ]


def pretty(signal: Set[str], gaps: bool = True) -> str:
    out = []
    for letter in ALL_LETTERS:
        if letter in signal:
            out.append(letter)
        elif gaps:
            out.append(" ")
        else:
            out.append("")
    return "".join(out)


def is_simple(m: Dict[str, Set[str]]) -> bool:
    return all(
        len(v) == 1
        for k, v in m.items()
    )


def simplify_mapping(m: Dict[str, Set[str]]) -> None:
    while not is_simple(m):
        for letter in ALL_LETTERS:
            possible_segments = m[letter]
            if len(possible_segments) == 1:
                (segment,) = possible_segments
                for other_letter in ALL_LETTERS.replace(letter, ""):
                    m[other_letter].discard(segment)


if __name__ == "__main__":

    segments = [
        (
            sorted(
                ((signal, get_possible_numbers(signal)) for signal in signals.split(" ")),
                key=lambda s_v: len(s_v[1]),
            ),
            [sorted(output) for output in outputs.split(" ")]
        )
        for line in fileinput.input()
        for signals, outputs in (line.strip().split(" | "),)
    ]

    # total_unique = sum(
    #     1
    #     for signals, outputs in segments
    #     for output in outputs
    #     if len(get_possible_numbers(output)) == 1
    # )
    # print("Part 1:", total_unique)

    total = 0
    for signals, outputs in segments:
        letter_to_possible_segments = {
            letter: set()
            for letter in "abcdefg"
        }
        digit_to_possible_signals = {
            d: []
            for d in [1, 7, 4, 2, 0, 8]
        }
        for signal, possible_digits in signals:
            for digit in possible_digits:
                if digit in digit_to_possible_signals:
                    digit_to_possible_signals[digit].append(set(signal))

        for digit, possible_signals in digit_to_possible_signals.items():
            actual_common = LENGTH_TO_COMMON_SEGMENTS[DIGIT_TO_LENGTH[digit]]
            signal_common = reduce(operator.and_, possible_signals)

            for letter in signal_common:
                if not letter_to_possible_segments[letter]:
                    letter_to_possible_segments[letter] = set(actual_common)
                else:
                    letter_to_possible_segments[letter] &= actual_common

        simplify_mapping(letter_to_possible_segments)

        actual_to_scrambled = {
            s: k
            for k, v in letter_to_possible_segments.items()
            for s in v
        }

        segment_to_digit = {
            pretty({actual_to_scrambled[l] for l in DIGIT_TO_SEGMENTS[n]}, gaps=False): n
            for n in range(0, 10)
        }

        digits = [
            str(segment_to_digit[pretty(set(output), gaps=False)])
            for output in outputs
        ]
        total += int("".join(digits))

    print("Part 2:", total)
