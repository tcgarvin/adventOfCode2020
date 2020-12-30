from rich import print
from rich.progress import track

from itertools import chain

class Cup:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None

    def __repr__(self):
        return f"Cup({self.value})"
        

class Cups:
    def __init__(self, initial_positions):
        self.index = {}
        self.max_value = max(initial_positions)
        positions = initial_positions

        first_cup = None
        previous_cup = None
        for value in positions:
            cup = Cup(value)
            self.index[value] = cup
            if first_cup is None:
                first_cup = cup

            if previous_cup is not None:
                previous_cup.next = cup
                cup.previous = previous_cup

            previous_cup = cup

        first_cup.previous = previous_cup
        previous_cup.next = first_cup
        self.current_cup = first_cup

    def step(self):
        #print(self)
        pick_up_start = self.current_cup.next
        pick_up_end = pick_up_start.next.next

        # Trim out the cups to be picked up
        self.current_cup.next = pick_up_end.next
        pick_up_end.next.previous = self.current_cup

        # Find destination
        destination_value = self.current_cup.value - 1
        if destination_value == 0:
            destination_value = self.max_value

        pick_up_values = tuple(cup.value for cup in (pick_up_start, pick_up_start.next, pick_up_end))
        check_pick_up_for_destination = True
        while check_pick_up_for_destination:
            check_pick_up_for_destination = False
            if destination_value in pick_up_values:
                destination_value -= 1
                if destination_value == 0:
                    destination_value = self.max_value
                check_pick_up_for_destination = True

        #print(pick_up_values, destination_value)

        destination = self.index[destination_value]

        # Splice picked-up values in after destination
        destination_end = destination.next
        destination.next = pick_up_start
        pick_up_start.previous = destination
        destination_end.previous = pick_up_end
        pick_up_end.next = destination_end

        self.current_cup = self.current_cup.next

    def __str__(self):
        output = []
        cup = self.current_cup
        output.append(str(cup.value))
        cup = cup.next
        while cup is not self.current_cup:
            output.append(str(cup.value))
            cup = cup.next

        return "".join(output)
        

def solve_part_1(initial_positions):
    cups = Cups(initial_positions)
    for i in range(100):
        cups.step()

    cup_one = cups.current_cup
    while cup_one.value != 1:
        cup_one = cup_one.next

    result = []
    cup = cup_one.next
    while cup.value != 1:
        result.append(str(cup.value))
        cup = cup.next

    return "".join(result)

def solve_part_2(initial_positions, length=1000000, moves=10000000):
    positions = list(initial_positions)
    for value in range(max(initial_positions) + 1, length + 1):
        positions.append(value)

    cups = Cups(positions)

    for i in track(range(moves)):
        cups.step()

    cup_one = cups.index[1]
    return cup_one.next.value * cup_one.next.next.value

if __name__ == "__main__":
    puzzle_input = [int(c) for c in "364297581"]
    #puzzle_input = [int(c) for c in "389125467"]

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")