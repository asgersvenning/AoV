from helpers import get_path, get_lines

## Visualization
import colorama
BLUE, YELLOW, RED = colorama.Back.BLUE, colorama.Back.YELLOW, colorama.Back.RED
RESET = colorama.Back.RESET

def visualize_selection(bank, indices : list[int], colors : list[str]=[BLUE, YELLOW, RED]):
    bank_ : list = bank.copy()
    n = len(indices)
    for i in reversed(list(range(n))):
        idx = indices[i]
        if i == 0:
            color = colors[0]
        elif i == (n - 1):
            color = colors[2]
        else:
            color = colors[1]
        bank_.insert(idx+1, RESET)
        bank_.insert(idx, color)
    print("".join(map(str, bank_)))
## End visualization

def parse_input(lines : list[str]):
    return [list(map(int, line)) for line in lines]

input = parse_input(get_lines(get_path("input")))

# Part 1
def argmax(x : list[int]):
    if len(x) == 0:
        raise RuntimeError("?", x)
    i, m = 0, x[0]
    for j, v in enumerate(x[1:]):
        if v > m:
            m = v
            i = j + 1
    return i
    
def max_voltage(bank : list[int], n : int=2, visualize=False):
    ls = [-1]
    for i in range(n):
        ls.append(argmax(bank[(ls[-1]+1):((i-n+1) or len(bank))]) + ls[-1] + 1)
    ls = ls[1:]
    if visualize:
        visualize_selection(bank, ls)
    return int("".join(map(str, map(bank.__getitem__, ls))))

def part1(banks : list[list[int]]):
    return sum(map(max_voltage, banks))

print("Part 1:", part1(input)) # = 17144

# Part 2
def part2(banks : list[list[int]]):
    return sum(map(lambda x : max_voltage(x, 12, False), banks))

print("Part 2:", part2(input)) # = 170371185255900