from rich import print
from rich.table import Table

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


def text_to_range(text):
    return tuple(map(int, text.split("-"))) 


def class_to_ranges(clazz):
    return (text_to_range(clazz.group("range1")), text_to_range(clazz.group("range2")))


def is_in_range(field_value, class_range):
    low, high = class_range
    return field_value >= low and field_value <= high


def solve_part_1(classes, my_ticket, nearby_tickets):
    ranges = []
    for clazz in classes:
        ranges.extend(class_to_ranges(clazz))

    invalid_ticket_field_values = []
    valid_tickets = []
    for ticket in nearby_tickets:
        is_valid = True
        for field_value in ticket:
            in_range = False
            for class_range in ranges: 
                if is_in_range(field_value, class_range):
                    in_range = True
                    break

            if not in_range:
                invalid_ticket_field_values.append(field_value)
                is_valid = False

        if is_valid:
            valid_tickets.append(ticket)

    return sum(invalid_ticket_field_values), valid_tickets
    
def solve_part_2(valid_tickets, classes, my_ticket, nearby_tickets):
    class_names = set(map(lambda match: match.group("name"), classes))
    #print(class_names)

    column_possibilities = [set(class_names) for _ in range(20)]

    ranges = {clz.group("name"): class_to_ranges(clz) for clz in classes}

    #print(len(valid_tickets))
    for ticket in valid_tickets:
        for i, value in enumerate(ticket):
            possible_classes = column_possibilities[i]
            for class_name in list(possible_classes):
                range1, range2 = ranges[class_name]
                if (not is_in_range(value, range1)) and (not is_in_range(value, range2)):
                    #print(f"{value} is not in {range1} or {range2}. Removing {class_name} from {i}")
                    possible_classes.remove(class_name)

    columns = [clz.group("name") for clz in classes]
    table = Table(show_lines=True)
    table.add_column("Field Name")
    for i in range(20):
        table.add_column(str(i))

    class_names = sorted(
        class_names, 
        key=lambda name: sum(name in column_possibilities[i] for i in range(20))
     )

    class_column_map = {}
    for name in class_names:
        row_values = []
        for i in range(20):
            show_char = " "
            if name in column_possibilities[i]:
                show_char = "X"
                if i not in class_column_map.values():
                    show_char = "✓"
                    class_column_map[name] = i

            row_values.append(show_char)
        table.add_row(name, *row_values)

    print(table)

    total = 1
    for classname, column_number in class_column_map.items():
        if classname.startswith("departure"):
            total *= my_ticket[column_number]

    return total

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
                my_ticket = list(map(int, line.split(",")))

            elif mode == 2:
                nearby_tickets.append(list(map(int, line.split(","))))

    return classes, my_ticket, nearby_tickets

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1, valid_tickets = solve_part_1(*puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(valid_tickets, *puzzle_input)
    print(f"Part 2: {answer_2}")