from operator import add, mul
from rich import print

class Value:
    def get_value(self):
        pass

    def get_value_2(self):
        pass

class SingleValue(Value):
    def __init__(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def get_value_2(self):
        return self._value

    def __repr__(self):
        return f"<SingleValue({self._value})>"

class Expression(Value):
    def __init__(self):
        self._terms = []
        self._operations = []

    def add_term(self, term):
        if len(self._terms) > len(self._operations):
            print(self._terms, self._operations, term)
            raise Exception("Expected operation, got term")

        self._terms.append(term)

    def add_operation(self, operation):
        if len(self._operations) >= len(self._terms):
            print(self._terms, self._operations, operation)
            raise Exception("Expected term, got operation")

        self._operations.append(operation)

    def get_value(self):
        if len(self._terms) != len(self._operations) + 1:
            print(self._terms, self._operations)
            raise Exception(f"Expected one more terms than operations. Instead, have {len(self._terms)} terms and {len(self._operations)} operations")

        accumulator = self._terms[0].get_value()
        for i, operation in enumerate(self._operations):
            accumulator = operation(accumulator, self._terms[i+1].get_value())

        return accumulator

    def get_value_2(self):
        if len(self._terms) != len(self._operations) + 1:
            print(self._terms, self._operations)
            raise Exception(f"Expected one more terms than operations. Instead, have {len(self._terms)} terms and {len(self._operations)} operations")

        terms = self._terms[:]
        operations = self._operations[:]

        while len(operations) > 0:
            i = None
            try:
                i = operations.index(add)
            except ValueError:
                i = operations.index(mul)

            operation = operations.pop(i)
            operation_result = operation(terms[i].get_value_2(), terms[i+1].get_value_2())
            terms[i : i+2] = [SingleValue(operation_result)]

        assert len(terms) == 1
        return terms[0].get_value_2()


DIGITS = tuple([str(i) for i in range(10)])
OPERATIONS = {
    "+": add,
    "*": mul
}

def parse_expression(line, start_index=0):
    expression = Expression()

    i = start_index
    while i < len(line):
        char = line[i]
        if char in DIGITS:
            expression.add_term(SingleValue(int(char)))

        elif char in OPERATIONS:
            expression.add_operation(OPERATIONS[char])

        elif char == "(":
            subexpression, last_i = parse_expression(line, i+1)
            expression.add_term(subexpression)
            i = last_i

        elif char == ")":
            break

        i += 1

    return expression, i


def solve_part_1(puzzle_input):
    expressions = []
    for line in puzzle_input:
        expression, _ = parse_expression(line)
        expressions.append(expression)

    total = sum((e.get_value() for e in expressions))

    return total, expressions

def solve_part_2(expressions):
    total = sum((e.get_value_2() for e in expressions))
    return total

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(line)
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1, expressions = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(expressions)
    print(f"Part 2: {answer_2}")