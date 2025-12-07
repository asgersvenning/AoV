from collections import defaultdict

import numpy as np
from helpers import get_lines, get_path

SYMBOLS = {
    "." : 0,
    "^" : 1,
    "S" : -1,
    "|" : 2
}

## Visualization
import colorama

BLACK, YELLOW, RED, BLUE, RESET = list(map(colorama.Fore.__getattribute__, ["BLACK", "YELLOW", "RED", "BLUE", "RESET"]))

RENDERED_SYMBOLS = {
    0 : f'{BLACK}.{RESET}',
    1 : f'{RED}^{RESET}',
    -1 : f'{YELLOW}S{RESET}',
    2 : f'{BLUE}|{RESET}'
}

def render(state : np.ndarray):
    return "\n".join("".join(map(RENDERED_SYMBOLS.get, row)) for row in state)
## End visualization

def parse_input(input : list[str]):
    return np.array([list(map(SYMBOLS.get, line)) for line in input])

input = parse_input(get_lines(get_path("input")))

# Part 1
def advance(state : np.ndarray, beams : list[tuple[int, int, int]]):
    new_beams, splits = [], 0
    for (x, y, n) in beams:
        nx, ny = x, y + 1
        if y >= state.shape[1]:
            continue
        cond = state[ny, nx]
        if cond == 0:
            new_beams.append((nx, ny, n))
        elif cond == 1:
            splits += 1
            nxl, nxr = nx - 1, nx + 1
            if nxl >= 0:
                new_beams.append((nxl, ny, n))
            if nxr < state.shape[1]:
                new_beams.append((nxr, ny, n))
    counts = defaultdict(lambda : 0)
    for (x, y, n) in new_beams:
        counts[(x, y)] += n
    beams = [tuple((*k, v)) for k, v in counts.items()]
    for (x, y, n) in beams:
        state[y, x] = 2
    return state, beams, splits

def part1(state : np.ndarray):
    beams, splits = [tuple(np.concatenate(np.nonzero(state == -1)).flatten().tolist()[::-1] + [1])], 0
    while beams:
        state, beams, this_splits = advance(state, beams)
        splits += this_splits
    return splits
    
print("Part 1:", part1(input.copy())) # = 1678

# Part 2
def part2(state : np.ndarray):
    beams, max_beams = [tuple(np.concatenate(np.nonzero(state == -1)).flatten().tolist()[::-1] + [1])], 0
    while beams:
        state, beams, _ = advance(state, beams)
        max_beams = max(max_beams, sum(b[-1] for b in beams))
    return max_beams
    
print("Part 2:", part2(input.copy())) # = 357525737893560
    
    
    
    