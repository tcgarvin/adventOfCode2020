from rich import print

from functools import reduce
from itertools import chain
import re

LINE_RE = re.compile("""
    ^
    (?P<ingredients>[^(]+)
    (?:
    [(]contains
    (?P<allergens>[^)]+)
    [)]
    )?
    $
""", re.X)

def solve_part_1(puzzle_input):
    all_ingredients = set()
    allergen_candidates = dict()
    for ingredients, allergens in puzzle_input:
        all_ingredients |= ingredients

        for allergen in allergens:
            if allergen not in allergen_candidates:
                allergen_candidates[allergen] = set(ingredients)
            else:
                allergen_candidates[allergen].intersection_update(ingredients)

    #print(allergen_candidates)
    #print(len(all_ingredients))

    all_candidates = set(chain.from_iterable(allergen_candidates.values()))
    confirmed_safe = all_ingredients - all_candidates

    result = 0
    for ingredients, _ in puzzle_input:
        result += len(ingredients & confirmed_safe)
    return result, allergen_candidates

def solve_part_2(allergen_candidates):
    final_allergens = {}

    finished = False
    while not finished:
        for allergen, candidates in allergen_candidates.items():
            trimmed_candidates = candidates.difference(final_allergens.values())
            #print(allergen, candidates, trimmed_candidates)
            if len(trimmed_candidates) == 1:
                final_allergens[allergen] = trimmed_candidates.pop()

        if len(final_allergens) == len(allergen_candidates):
            finished = True

    result = []
    for allergen in sorted(final_allergens.keys()):
        result.append(final_allergens[allergen])
    return ",".join(result)

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            match = LINE_RE.match(line.strip())
            if match is None:
                print(f"Cannot match: {line}")
            ingredients = set(match.group("ingredients").strip().split())
            allergens = set(match.group("allergens").strip().replace(",","").split())
            puzzle_input.append((ingredients, allergens))
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1, allergen_candidates = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(allergen_candidates)
    print(f"Part 2: {answer_2}")