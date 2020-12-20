from rich import print

import re

FILLER_LINES = ("your ticket:", "nearby tickets:")

CLASS_RE = re.compile("""
    ^
    (?P<name>[^:]+)
    :[ ]
    (?P<range1>[0-9]+-[0-9]+)
    [ ]or[ ]
    (?P<range2>[0-9]+-[0-9]+)
    $
""", re.X)

def solve_part_1(classes, my_ticket, nearby_tickets):
    ranges = []
    for clazz in classes:
        ranges.append(tuple(map(int, clazz.group("range1").split("-"))))
        ranges.append(tuple(map(int, clazz.group("range2").split("-"))))

    invalid_ticket_field_values = []
    valid_tickets = []
    for ticket in nearby_tickets:
        is_valid = True
        for field_value in ticket:
            in_range = False
            for low,high in ranges: 
                if field_value >= low and field_value <= high:
                    in_range = True
                    break

            if not in_range:
                invalid_ticket_field_values.append(field_value)
                is_valid = False

        if is_valid:
            valid_tickets.append(ticket)

    return sum(invalid_ticket_field_values), valid_tickets
    
def solve_part_2(valid_tickets, classes, my_ticket, nearby_tickets):
    return ""

def get_puzzle_input():
    classes = []
    my_ticket = None
    nearby_tickets = []
    with open("input.txt") as input_txt:
        mode = 0
        for line in input_txt:
            if line.strip() in FILLER_LINES:
                continue

            elif len(line.strip()) == 0:
                mode += 1

            elif mode == 0:
                classes.append(CLASS_RE.match(line))

            elif mode == 1:
                my_ticket = map(int, line.split(","))

            elif mode == 2:
                nearby_tickets.append(map(int, line.split(",")))

    return classes, my_ticket, nearby_tickets

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1, valid_tickets = solve_part_1(*puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(valid_tickets, *puzzle_input)
    print(f"Part 2: {answer_2}")