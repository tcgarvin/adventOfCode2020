from rich import print

def solve_part_1(timestamp, busses):
    best_wait = timestamp
    best_bus = None
    for bus in busses:
        if bus == 0:
            continue

        wait = bus - timestamp % bus
        if wait < best_wait:
            best_wait = wait
            best_bus = bus

    #print(best_wait, best_bus)

    return best_wait * best_bus

def solve_part_2(timestamp, busses):
    priority_list = []
    for offset, bus in enumerate(busses):
        if bus == 0:
            continue
        priority_list.append((bus, offset))

    priority_list = sorted(priority_list, reverse=True)
    print(priority_list)

    base_bus, base_offset = priority_list.pop(0)

    match = False
    candidate = -base_offset
    while match == False:
        candidate += base_bus
        match = True
        for bus, offset in priority_list:
            if (candidate + offset) % bus != 0:
                match = False
                break
            else:
                print(bus, candidate)

    return candidate

def get_puzzle_input():
    timestamp = None
    busses = []
    with open("input.txt") as input_txt:
        timestamp = int(input_txt.readline())
        busses = input_txt.readline().split(",")
        busses = list(map(lambda b: 0 if b == "x" else int(b), busses))
    return timestamp, busses

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()
    print(puzzle_input)

    answer_1 = solve_part_1(*puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(*puzzle_input)
    print(f"Part 2: {answer_2}")