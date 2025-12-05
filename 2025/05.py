from helpers import get_path, get_lines

def parse_input(lines : list[str]) -> tuple[list[tuple[int, ...]], list[int]]:
    ranges, available = [], []
    isRange = True
    for line in lines:
        if not line:
            isRange = False
            continue
        if isRange:
            ranges.append(tuple(map(int, line.split("-"))))
        else:
            available.append(int(line))
    return ranges, available

input = parse_input(get_lines(get_path("input")))

# Part 1
def part1(ranges : list[tuple[int, ...]], available : list[int]):
    return sum(any(r[0] <= ingredient <= r[1] for r in ranges) for ingredient in available)

print("Part 1:", part1(*input)) # = 865

# Part 2
overlaps, merge = lambda r00, r01, r10, r11 : r00 <= r11 and r10 <= r01, lambda ranges : tuple(fn(map(fn, ranges)) for fn in [min, max])
print("Part 2:", sum((r - l) + 1 for l, r in new) if ([new.__setitem__(-1, merge((r1, r2))) if overlaps(*(r1 := new[-1]), *(r2 := ranges.pop(0))) else new.append(r2) for _ in range(len(ranges))] and new if ((ranges := sorted(ranges := input[0])) and (new := [ranges.pop(0)])) else None) else None) # = 352556672963116
