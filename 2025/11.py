from helpers import get_lines, get_path
from functools import lru_cache

def parse_input(input : list[str]):
    parse_one = lambda x : (x[:3], tuple([x[(5+i*4):(5+(i+1)*4-1)] for i in range((len(x) - 4)//4)]))
    return dict(map(parse_one, input))

input = parse_input(get_lines(get_path("input")))

# Part 1
def part1(connections : dict[str, tuple[str, ...]], start : str="you"):
    return sum(1 if nxt == "out" else part1(connections, nxt) for nxt in connections[start])

print("Part 1:", part1(input)) # = 571

# Part 2
def part2(connections : dict[str, tuple[str, ...]]):
    PROBLEMS = ("dac", "fft")
    @lru_cache(None, True)
    def inner(start : str, state : tuple):
        return sum(state == PROBLEMS if nxt == "out" else inner(nxt, state if not nxt in PROBLEMS else tuple(sorted((*state, nxt)))) for nxt in connections[start])
    return inner("svr", tuple())

print("Part 2:", part2(input)) # = 511378159390560