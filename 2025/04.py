from helpers import get_path, get_lines

import numpy as np

## Visualization
import colorama

BLACK, BLUE, RED, YELLOW, RESET = colorama.Fore.BLACK, colorama.Fore.BLUE, colorama.Fore.RED, colorama.Fore.YELLOW, colorama.Fore.RESET

def color(o, c):
    return str(o)
    # return f'{c}{o}{RESET}'

def element(c : str):
    match c:
        case 0:
            return color(".", BLACK)
        case 1:
            return color("@", RED)
        case -1:
            return color("+", BLUE)
        case _:
            return color(c, YELLOW)

## End visualization

class Area:
    def __init__(self, input : list[str]):
        self.width = len(input[0])
        self.height = len(input)

        self.data = np.array([[0 if c == "." else 1 for c in line] for line in input], int)

    def __len__(self):
        return np.count_nonzero(self.data)

    @property
    def rolls(self):
        nz = np.nonzero(self.data)
        return np.array(nz).transpose(1, 0)

    def __str__(self):
        return "\n".join(["".join(map(element, row)) for row in self.data])

input = get_lines(get_path("input"))

# Part 1
def neighbors(x : int, y : int, w : int, h : int):
    xmi = int(max(x-1, 0))
    xma = int(min(x+2, h))
    ymi = int(max(y-1, 0))
    yma = int(min(y+2, w))
    return np.array(np.meshgrid(np.arange(xmi, xma), np.arange(ymi, yma)))

def part1(area : Area):
    for roll in area.rolls:
        ne = neighbors(*roll, area.width, area.height)
        adj = (area.data[*ne] != 0).sum().item() - 1
        if adj < 4:
            area.data[*roll] = -1
    return (area.data == -1).sum().item()


print("Part 1:", part1(Area(input))) # = 1409

# Part 2
# from helpers import Animation

def part2(area : Area):
    start = len(area)
    # anim = Animation()
    while part1(area) > 0:
        # anim += str(area)
        area.data[area.data == -1] = 0
    # anim(0.1, transient=False)
    end = len(area)
    return start - end

print("Part 2:", part2(Area(input))) # = 8366
