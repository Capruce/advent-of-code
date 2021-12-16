from collections import defaultdict
import fileinput
from typing import Dict, List, Tuple


Element = str
Pair = Tuple[str, str]
Chain = Dict[Pair, int]
ReactionMap = Dict[Pair, Tuple[Pair, Pair]]


def load_input() -> Tuple[Element, Chain, ReactionMap]:
    lines: List[str] = list(fileinput.input())

    first_line = lines[0].strip()
    template: Chain = defaultdict(int)
    for pair in zip(first_line[:-1], first_line[1:]):
        template[pair] += 1

    pair_to_new_pairs = {
        (left, right): ((left, target), (target, right))
        for line in lines[2:]
        for (left, right), target in (line.strip().split(" -> "),)
    }

    return first_line[0], template, pair_to_new_pairs


def step(chain: Chain, pair_to_pairs: ReactionMap) -> Chain:
    new_chain = defaultdict(int)
    for pair, count in chain.items():
        r1, r2 = pair_to_pairs[pair]
        new_chain[r1] += count
        new_chain[r2] += count

    return new_chain


def n_steps(chain: Chain, reaction_map: ReactionMap, steps: int) -> Chain:
    next_chain = chain
    for _ in range(steps):
        next_chain = step(next_chain, reaction_map)
    return next_chain


def get_difference(chain: Chain, first_element: str) -> int:
    element_to_count = defaultdict(int)
    for (_, right), count in chain.items():
        element_to_count[right] += count

    element_to_count[first_element] += 1

    counts = sorted(element_to_count.values())
    return counts[-1] - counts[0]


if __name__ == "__main__":
    FIRST_ELEMENT, TEMPLATE, PAIR_TO_PAIRS = load_input()

    print("Part 1:", get_difference(n_steps(TEMPLATE, PAIR_TO_PAIRS, 10), FIRST_ELEMENT))
    print("Part 2:", get_difference(n_steps(TEMPLATE, PAIR_TO_PAIRS, 40), FIRST_ELEMENT))
