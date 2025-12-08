from math import prod

import numpy as np
from helpers import get_lines, get_path


def parse_input(input : list[str]):
    return np.array([list(map(int, line.split(","))) for line in input], int)

input = parse_input(get_lines(get_path("input")))

# Part 1 & 2
def solve(junctions : np.ndarray, it : int | None=None, part2 : bool=False):
    od = (od := np.vstack(((od := np.argsort(d := np.linalg.norm(junctions[np.newaxis, ...] - junctions[:, np.newaxis, ...], 2, 2), None)) // len(d), od % len(d))).T)[od[:,0] != od[:, 1]][::2]
    j2c : dict[tuple[int, int], int] = {j : i for i, j in enumerate(junctions)} if (junctions := [tuple(j.tolist()) for j in junctions]) else None
    c2j : dict[int, list[tuple[int, int]]] = {v : [k] for k, v in j2c.items()}
    i, it = len(junctions) - 1, it or len(od)
    for ep, _ in zip(od, range(it)):
        cp = [j2c[j] for j in jp] if (jp := [junctions[e] for e in ep]) else None
        if cp[0] != cp[1] and (ljp := jp):
            [j2c.__setitem__(j, i) for j in c] if c2j.__setitem__(i := i + 1, c := sum(map(c2j.pop, cp), start=[])) is None else None
    for c in (circuits := {c : [] for c in set(j2c.values())}):
        circuits[c].extend([k for k, v in j2c.items() if v == c])
    return ljp[0][0] * ljp[1][0] if part2 else prod(sorted(map(len, circuits.values()))[-3:])

# Part 1
print("Part 1:", solve(input, 1000, False)) # = 117000

# Part 2
print("Part 2:", solve(input, None, True)) # = 8368033065