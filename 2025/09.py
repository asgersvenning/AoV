from helpers import get_lines, get_path
from math import prod
from operator import le, ge

def parse_input(input : list[str]) -> list[tuple[int, int]]:
    return [tuple(map(int, line.split(","))) for line in input]

input = parse_input(get_lines(get_path("input")))

# Part 1
def boxsize(pt0 : tuple[int, int], pt1 : tuple[int, int]):
    return prod(abs(c0 - c1) + 1 for c0, c1 in zip(pt0, pt1))

def part1(points : list[tuple[int, int]]):
    return max(boxsize(points[i], points[j]) for i in range(n) for j in range(i+1, n)) if (n := len(points)) else 0

print("Part 1:", part1(input)) # = 4750176210

# Part 2
def valid(i : int, j : int, points : list[tuple[int, int]]):
    return not any((box[0] < pt[0] < box[2]) and (box[1] < pt[1] < box[3]) for pt in points) if (box := [fn(c) for fn in [min, max] for c in zip(points[i], points[j])]) else None

def outliers(points : list[tuple[int, int]]):
    return [i for i in range(len(points)) if min(boxsize(points[i], points[(i + 2) % len(points)]), boxsize(points[i], points[(i - 2) % len(points)])) > 50000000]

def best_rectangle(points : list[tuple[int, int]], mb=0):
    return [(i, j) for i in range(len(points)) for j in range(i + 1, len(points)) if (b := boxsize(points[i], points[j])) >= mb and valid(i, j, points) and (mb := b)][-1]

def part2(points : list[tuple[int, int]]):
    si = [[i for i, p in enumerate(points) if op(p[1], points[o][1])] for o, op in zip(outliers(points), (ge, le))]
    return max(boxsize(points[p], points[q]) for p, q in [[i[k] for k in j] for i, j in zip(si, map(best_rectangle, [[points[i] for i in s] for s in si]))])

print("Part 2:", part2(input)) # = 1574684850