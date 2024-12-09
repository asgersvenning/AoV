def parse_input(path):
    with open(path, "r") as f:
        return [[int(c) for c in line.strip().replace(":", "").split(" ")] for line in f.readlines()]

class Equation:
    def __init__(self, values, part2=False):
        self.result, self.values, self.OPERATORS = values[0], values[1:], [lambda x, y : x + y, lambda x, y : x * y]
        if part2:
            self.OPERATORS.append(lambda x, y : int(f'{x}{y}'))

    def __len__(self):
        return len(self.values) - 1
    
    def test(self):
        def _inner(init=0, i=0):
            values = self.values[i:]
            if len(values) == 0:
                return init == self.result
            if init > self.result:
                return False
            return any([_inner(op(init, values[0]), i+1) for op in self.OPERATORS])
        
        return _inner(self.values[0], 1)
    
    def __repr__(self):
        return str(self.result) + " = " + " x ".join(map(str, self.values))

def solution(data, part : int=1):
    return sum([calibration.result for line in data if (calibration := Equation(line, part2=part==2)).test()])    

# print(part1(parse_input("2024/inputs/07.test"), 1))
print(solution(parse_input("2024/inputs/07.input"), 1))

# print(part2(parse_input("2024/inputs/07.test"), 2))
print(solution(parse_input("2024/inputs/07.input"), 2))