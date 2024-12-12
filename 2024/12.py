import colorama

SQUARE = "■"
CIRCLE = "●"
TRIANGLE = "▲"
DIAMOND = "◆"
SYMBOLS = [SQUARE, CIRCLE, TRIANGLE, DIAMOND]

BLACK, GREEN, RED, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET = colorama.Fore.BLACK, colorama.Fore.GREEN, colorama.Fore.RED, colorama.Fore.YELLOW, colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.CYAN, colorama.Fore.WHITE, colorama.Fore.RESET
COLORS = [GREEN, RED, YELLOW, BLUE, MAGENTA, CYAN, BLACK, WHITE]

from helpers import get_path, get_lines

def parse_input(type : str):
    return [list(line) for line in get_lines(get_path(type))]

def get_unique(garden : list[list[str]]):
    return sorted(set(plot for row in garden for plot in row))

def pretty_print(garden : list[list[str]]):
    unique_crops = get_unique(garden)
    crop_colors = {crop : COLORS[i % len(COLORS)] for i, crop in enumerate(unique_crops)}
    crop_symbols = {crop : SYMBOLS[(i // len(SYMBOLS)) % len(SYMBOLS)] for i, crop in enumerate(unique_crops)}
    def color_crop(crop : str):
        if crop.isdigit():
            return "○"
        return f'{crop_colors[crop]}{crop_symbols[crop]}{RESET}'
    print("\n".join(" ".join(map(color_crop, row)) for row in garden))

def floodfill(garden : list[list[str]], init : tuple=(0,0), crop : str=".", escape="0"):
    i, j = init
    if crop == ".":
        crop = garden[i][j]
    if crop != garden[i][j]:
        return (crop, 0 if garden[i][j] == escape else 1, [])
    garden[i][j] = escape
    positions = [init]
    perimeter = 0
    dis = [0]
    if i > 0:
        dis.append(-1)
    else:
        perimeter += 1
    if i < (len(garden) - 1):
        dis.append(1)
    else:
        perimeter += 1
    djs = [0]
    if j > 0:
        djs.append(-1)
    else:
        perimeter += 1
    if j < (len(garden) - 1):
        djs.append(1)
    else:
        perimeter += 1
    for di in dis:
        for dj in djs:
            if (dj == 0) == (di == 0):
                continue
            other = floodfill(garden, (i + di, j + dj), crop, escape)
            perimeter += other[1]
            positions += other[2]
    return crop, perimeter, positions

def regions(garden : list[list[str]]):
    garden = [[plot for plot in row] for row in garden]
    regions, crops = [], get_unique(garden)
    for i, row in enumerate(garden):
        for j, plot in enumerate(row):
            if plot not in crops:
                continue
            regions.append(floodfill(garden, (i, j), escape=f'{len(regions)}'))
    return regions

def part1(garden : list[list[str]], verbose : bool=False):
    solution = sum(perimeter * len(plots) for _, perimeter, plots in regions(garden))
    if verbose:
        print("GARDEN:")
        pretty_print(garden)
        format_output = [(crop, f'{len(plots):>4} * {perimeter:<4} = {perimeter * len(plots):<8}') for crop, perimeter, plots in regions(garden)]
        for crop, price in format_output:
            print(f'{crop}: ', price)
        print("SOLUTION:", solution)
    return solution

# part1(parse_input("test"), verbose=True)
print(part1(parse_input("input")))

def directions():
    return [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1]]

turns = directions()

def remove_inside(region : list[tuple[int, int]]):
    removers = []
    for idx, (i, j) in enumerate(region):
        if all((i + di, j + dj) in region for di, dj in turns):
            removers.append(idx)
    while removers:
        region.pop(removers.pop())
    return region

DIRECTIONS = {
    "right" : (0, 1),
    "down" : (1, 0),
    "left" : (0, -1),
    "up" : (-1, 0)
}
INV_DIRECTION = {f'{di},{dj}' : name for name, (di, dj) in DIRECTIONS.items()}

ORDER = {
    "right" : ["up", "right", "down", "left"],
    "down" : ["right", "down", "left", "up"],
    "left" : ["down", "left", "up", "right"],
    "up" : ["left", "up", "right", "down"]
}

OPPOSITE = {
    "right" : "left",
    "down" : "up"
}
OPPOSITE.update({v : k for k, v in OPPOSITE.items()})


def points_are_neighbours(a : tuple[int, int], b : tuple[int, int]):
    return sum([abs(p - q) for p, q in zip(a, b)]) == 1

def points_are_equal(a : tuple[int, int], b : tuple[int, int]):
    return all([p == q for p, q in zip(a, b)])

def point_in_points(a : tuple[int, int], b : list[tuple[int, int]]):
    return any(points_are_equal(a, o) for o in b)

def connected_components(points : list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    components = {}
    idx = -1
    while points:
        idx += 1
        next = points.pop()
        combiners = []
        for i, component in components.items():
            if any(points_are_neighbours(next, other) for other in reversed(component)):
                combiners.append(i)
        if len(combiners) == 0:
            components[idx] = [next]
            continue
        selected = combiners.pop()
        components[selected].append(next)
        while combiners:
            components[selected] += components.pop(combiners.pop())
    return list(components.values())

def holes(region : list[tuple[int, int]]):
    i_s, j_s = map(set, zip(*region))
    min_i, max_i = min(i_s), max(i_s)
    min_j, max_j = min(j_s), max(j_s)
    holes : list[list[tuple[int, int]]] = []
    for component in connected_components([point for j in range(min_j - 2, max_j + 2) for i in range(min_i - 2, max_i + 2) if not point_in_points(point := (i, j), region)]):
        i_s, j_s = map(set, zip(*component))
        c_min_i, c_max_i = min(i_s), max(i_s)
        c_min_j, c_max_j = min(j_s), max(j_s)
        if not ((c_min_i <= min_i) or (c_min_j <= min_j) or (c_max_i >= max_i) or (c_max_j >= max_j)):
            holes.append(component)
    return holes

def simply_region(region : list[tuple[int, int]]):
    simple = []
    mi, mj = [min(map(lambda x : x[i], region)) for i in range(2)]
    region = [(i - mi, j - mj) for i, j in region]
    for i, j in region:
        i, j = (i + 1) * 2, (j + 1) * 2
        corners = [(i + di, j + dj) for di, dj in turns]
        for corner in corners:
            if corner not in simple:
                simple.append(corner)
    return simple

def sides(region : list[tuple[int, int]], can_have_holes : bool=True, debug : bool=False):
    if len(region) == 0:
        return 0, region
    region = sorted(region)
    if len(region) <= 2:
        return 4, region
    if len(set(i for i, _ in region)) == 1 or len(set(j for _, j in region)) == 1:
        return 4, region
    if len(region) == 3:
        return 6, region
    region = sorted(simply_region(region))
    if not can_have_holes and debug:
        print(stringify_contour(region)[0]) 
    direction, n_sides, order = "up", 0, [0]
    while True:
        ci, cj = region[order[-1]]
        neighbours = [region.index(neighbour) for di, dj in [DIRECTIONS[name] for name in ORDER[direction]] if point_in_points(neighbour := (ci + di, cj + dj), region)]
        if len(neighbours) == 0:
            raise RuntimeError()
        order.append(neighbours[0])
        ndirection = INV_DIRECTION[f'{region[order[-1]][0] - ci},{region[order[-1]][1] - cj}']
        if len(order) > 2 and order[:2] == order[-2:]:
            order.pop()
            if direction == "left":
                n_sides += 1
            break
        n_sides += 0 if direction == ndirection else 1# 2 if direction == OPPOSITE[ndirection] else 1
        if direction == OPPOSITE[ndirection]:
            raise RuntimeError()
        direction = ndirection
    if can_have_holes:
        n_inside_sides = sum(sides(hole, False, debug)[0] for hole in holes(region))
    else:
        n_inside_sides = 0
    return n_sides + n_inside_sides, [region[i] for i in order]

def stringify_contour(contour : list[tuple[int, int]], background : str = SQUARE, color : str = RED):
    mi, mj = [min(map(lambda x : x[i], contour)) for i in range(2)]
    contour = [(i - mi, j - mj) for i, j in contour]
    ui, uj = [max(map(lambda x : x[i], contour)) for i in range(2)]
    grid = [[color + background + RESET for _ in range(uj + 3)] for _ in range(ui + 3)]
    max_cell_size = 1
    for idx, (i, j) in enumerate(contour):
        i, j = i + 1, j + 1
        grid[i][j] = f'{idx},{grid[i][j]}' if background not in grid[i][j] else str(idx)
        max_cell_size = max(max_cell_size, len(grid[i][j]))
    return " " + ("\n" * 2 + " ").join("|".join([f'{colorama.Style.BRIGHT}{e: ^{max_cell_size + 2 + (len(e) - 1 if background in e else 0)}}{colorama.Style.RESET_ALL}' for e in row]) for row in grid), (max_cell_size + 3) * (uj + 3)

def part2(garden : list[list[str]], verbose : bool=False):
    solution = sum(sides(polygon)[0] * len(polygon) for _, _, polygon in regions(garden))
    # solution = None
    if verbose:
        for i, (crop, _, polygon) in enumerate(regions(garden)):
            # print(stringify_contour(polygon)[0])
            # print("###############################")
            n_side, contour = sides(polygon, debug=False)
            contour_str, width = stringify_contour(contour, crop, COLORS[:-1][i % (len(COLORS) - 1)])
            print(f'{f' {i = } SIDES = {n_side} ':_^{width}}')
            print(contour_str)
            print(f'{f'COST = {len(polygon)} * {n_side} = {len(polygon) * n_side}':-^{width}}')
        print("SOLUTION:", solution)
    return solution

# part2(parse_input("test0"), verbose=True)
# part2(parse_input("test1"), verbose=True)
# part2(parse_input("test2"), verbose=True)
# part2(parse_input("test3"), verbose=True)
# part2(parse_input("test"), verbose=True)
# for case in ["test1", "test0", "test2", "test3", "test"]:
#     print(part2(parse_input(case)))
# print(part2(parse_input("test4"), True))
print(part2(parse_input("input")))
