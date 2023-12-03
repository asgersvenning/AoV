class Simple:
    row: int
    col: int
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def __len__(self):
        raise NotImplementedError
    
    def distance(self, row, col):
        y_distance = abs(self.row - row)
        cols = [self.col + i for i in range(len(self))]
        x_distance = min([abs(i - col) for i in cols])
        return x_distance, y_distance
    
    def __sub__(self, other):
        return self.distance(other.row, other.col)
    
    def __str__(self):
        return f'Position: {self.col}, {self.row}'

class Number(Simple):
    value: int
    def __init__(self, row, col, number):
        super().__init__(row, col)
        self.value = int(number)

    def __len__(self):
        return len(str(self.value))
    
    def __str__(self):
        return super().__str__() + f' | Number: {self.value}'
    
class Symbol(Simple):
    def __init__(self, row, col, symbol):
        super().__init__(row, col)
        self.symbol = symbol

    def __len__(self):
        return 1
    
    def __str__(self):
        return super().__str__() + f' | Symbol: {self.symbol}'

digits = [str(i) for i in range(10)]
def parse_line(s, r):
    s = s.strip()
    parsing_number = False
    output = []
    for i, c in enumerate(s):
        if c == ".":
            pass
        elif not c in digits:
            output += [Symbol(r, i, c)]
        else:
            if parsing_number is False:
                parsing_number = i
            continue
        if not parsing_number is False:
            output += [Number(r, parsing_number, s[parsing_number:i])]
        parsing_number = False
    else:
        if not parsing_number is False:
            output += [Number(r, parsing_number, s[parsing_number:])]
    return output

class Schematic:
    def __init__(self, lines):
        self.rows = [parse_line(line, row) for row, line in enumerate(lines)]
        self.numbers = []
        self.symbols = []
        for row in self.rows:
            for item in row:
                if isinstance(item, Number):
                    self.numbers.append(item)
                elif isinstance(item, Symbol):
                    self.symbols.append(item)
                else:
                    raise TypeError(f'Item has class {type(item)} but expected Number or Symbol')

    def __str__(self):
        return "Numbers:\n" + "\n".join([str(i) for i in self.numbers]) + "\nSymbols:\n" + "\n".join([str(i) for i in self.symbols])
    
def is_adjacent(distance):
    x, y = distance
    if x > 1 or y > 1:
        return False
    if x == 0 and y == 0:
        return False
    return True

path = "inputs/03.input"

from math import prod

with open(path, "r") as file:
    input = Schematic(file.readlines())

    number_symbol_adjacency_matrix = [[is_adjacent(number - symbol) for symbol in input.symbols] for number in input.numbers]    
    numbers_adjacent = [any(i) for i in number_symbol_adjacency_matrix]

    print(sum([n.value for b, n in zip(numbers_adjacent, input.numbers) if b]))

    # Part 2
    gears = [s for s in input.symbols if s.symbol == "*"]

    gear_number_adjacency_matrix = [[is_adjacent(number - gear) for number in input.numbers] for gear in gears]    
    true_gears = [sum(i) == 2 for i in gear_number_adjacency_matrix]
    gears = [i for b, i in zip(true_gears, gears) if b]
    gear_number_adjacency_matrix = [[is_adjacent(number - gear) for number in input.numbers] for gear in gears]    

    gear_ratios = []
    for gear, neighbours in zip(gears, gear_number_adjacency_matrix):
        neighbour_values = []
        neighbour_numbers = [n for b, n in zip(neighbours, input.numbers) if b]
        for number in neighbour_numbers:
            neighbour_values += [number.value]
        if len(neighbour_values) != 2:
            raise ValueError(f"Unexpected format of neighbour_values: {neighbour_values}")
        gear_ratios += [prod(neighbour_values)]
    
    print(sum(gear_ratios))



