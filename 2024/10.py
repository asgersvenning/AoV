from helpers import get_lines, get_path

def parse_input(type : str):
    return list(list(map(int, line)) for line in get_lines(get_path(type)))

def format_data(data : list[list], sep : str="", width : int=1):
    return "\n".join(map(lambda x : sep.join(map(lambda y : f"{y:^{width}}", x)), data))

def get_trailheads(data : list[list[int]], trail_head : int=0) -> list[tuple[int, int]]:
    return [(i,j) for i, line in enumerate(data) for j, e in enumerate(line) if e == trail_head]

def search1(start : tuple[int, int], id : int, data : list[list[int]]):
    sy, sx, partial = len(data), len(data[0]), [[-1 for _ in line] for line in data]
    def inner(x : int, y : int, v : int=-1):
        if ((n := data[y][x]) - v) != 1 or partial[y][x] != -1: return
        if n == 9:
            partial[y][x] = id
            return
        partial[y][x] = 0
        [inner(nx, ny, n) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if ((dx == 0 or dy == 0) and (0 <= (nx := x + dx) < sx) and (0 <= (ny := y + dy) < sy))]
    return get_trailheads(partial, id) if inner(*start[::-1]) is None else []

def part1(data : list[list[int]]):
    return sum(len(search1(start, id, data)) for id, start in enumerate(get_trailheads(data), start=1))

# print(part1(parse_input("test")))
print(part1(parse_input("input")))

def search2(start : tuple[int, int], data : list[list[int]]):
    sy, sx, partial = len(data), len(data[0]), [[-1 for _ in line] for line in data]
    def inner(x : int, y : int, v : int=-1):
        if ((n := data[y][x]) - v) != 1: return 0
        partial[y][x] = 1 if n == 9 else partial[y][x]
        if (cached := partial[y][x]) != -1: return cached
        partial[y][x] = 0
        [partial[y].__setitem__(x, partial[y][x] + inner(nx, ny, n)) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if ((dx == 0 or dy == 0) and (0 <= (nx := x + dx) < sx) and (0 <= (ny := y + dy) < sy))]
        return partial[y][x]
    return inner(*start[::-1])

def part2(data : list[list[int]]):
    return sum(search2(start, data) for start in get_trailheads(data))

# print(part2(parse_input("test")))
print(part2(parse_input("input")))
