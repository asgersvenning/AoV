from helpers import get_lines, get_path, Animation

SYMBOLS = {
    "^" : 2,
    "#" : 1,
    "." : 0
}

CLI_SYMBOLS = {
    2 : "👷",
    1 : "🧱",
    0 : "🔵",
    -1 : "🔴",
    -2 : "🟡"
}

def parse_input(type : str):
    return [[SYMBOLS[c] for c in line.strip()] for line in get_lines(get_path(type))]

def get_objects(data : list[list[int]]):
    walls, guard = [], None
    walls : list[tuple[int, int]]
    for i, line in enumerate(data):
        for j, tile in enumerate(line):
            match tile:
                case 0:
                    pass
                case 1:
                    walls.append((i, j))
                case 2:
                    guard = [i, j, 1]
                case _:
                    raise ValueError("Unknown tile", tile, "found")
    if guard is None:
        raise RuntimeError("No guard found in data")
    return guard, walls

# Guard orientiation: LTRB
DELTA = {
    0 : [0, -1],
    1 : [-1, 0],
    2 : [0, 1],
    3 : [1, 0]
}

def pretty_print(data, guard, moves):
    data = [l.copy() for l in data]
    for move in moves:
        mi = move % len(data)
        mj = move // len(data)
        mt = data[mi][mj]
        if mt == 0:
            data[mi][mj] = -2
    i, j, d = guard
    di, dj = DELTA[d]
    ni, nj = i + di, j + dj
    try:
        if data[ni][nj] == 0:
            data[ni][nj] = -1
    except IndexError:
        pass
    return "\n".join(["".join([CLI_SYMBOLS[n] for n in line]) for line in data])

def move_guard(data, guard):
    i, j, d = guard
    di, dj = DELTA[d]
    ni, nj = i + di, j + dj
    try:
        if ni < 0 or nj < 0:
            raise IndexError
        tile = data[ni][nj]
    except IndexError:
        data[i][j] = 0
        return data, guard, False
    match tile:
        case 0:
            data[i][j] = 0
            guard[0] = ni
            guard[1] = nj
            data[ni][nj] = 2
        case 1:
            guard[-1] += 1
            if guard[-1] > 3:
                guard[-1] = 0
        case _:
            raise RuntimeError("Invalid tile", tile)
    return data, guard, True

def part1(board : list[list[int]], animate=False):
    guard, _ = get_objects(board)
    in_bounds, positions, frames = True, set(), []
    anim = Animation()
    if animate:
        anim += pretty_print(board, guard, positions)
    while in_bounds:
        positions.add(guard[0] + guard[1] * len(board))
        board, guard, in_bounds = move_guard(board, guard)
        if animate:
            anim += pretty_print(board, guard, positions)
    if animate:
        anim(0.05)
    return len(positions)

# part1(parse_input("test"), True)
print(part1(parse_input("input")))

def check_obstacle_ray(board : list[list[int]], guard : list[int]):
    i, j, d = guard
    ni, nj = DELTA[d]
    try:
        tile = board[i + ni][j + nj]
        if tile == 1:
            return False
    except IndexError:
        return False
    d += 1
    if d > 3:
        d = 0
    ni, nj = DELTA[d]
    tiles = []
    for k in range(1, len(board)):
        try:
            ti = i + ni * k
            tj = j + nj * k
            tile = board[ti][tj]
            tiles.append(tile)
        except IndexError:
            break
    return any(tile == 1 for tile in tiles)

def get_possible_obstacles(board : list[list[int]]):
    n = len(board)
    guard, _ = get_objects(board)
    in_bounds = True
    positions = {}
    while in_bounds:
        board, guard, in_bounds = move_guard(board, guard)
        if check_obstacle_ray(board, guard):
            move = guard[0] + guard[1] * len(board)
            if not move in positions:
                positions[move] = set()
            positions[move].add(guard[-1])
    possible_obstacles = []
    obstacle_collission = set()
    for move, dirs in positions.items():
        for d in dirs:
            mi = move % len(board)
            mj = move // len(board)
            di, dj = DELTA[d]
            wi = mi + di
            wj = mj + dj
            oh = wi + wj * n
            if oh in obstacle_collission:
                continue
            possible_obstacles.append([wi, wj])
            obstacle_collission.add(oh)
    return possible_obstacles

def check_cycle(board : list[list[int]], animate = False):
    guard, _ = get_objects(board)
    is_cycle, in_bounds, positions, n = False, True, {}, len(board)
    anim = Animation()
    if animate:
        anim += pretty_print(board, guard, positions)
    while in_bounds and not is_cycle:
        board, guard, in_bounds = move_guard(board, guard)
        if not in_bounds:
            break
        move = guard[0] + guard[1] * n
        if not move in positions:
            positions[move] = set()
        if guard[-1] in positions[move]:
            is_cycle = True
        positions[move].add(guard[-1])
        if animate:
            anim += pretty_print(board, guard, positions)
    if animate:
        anim(0.01)
    return is_cycle

def inner(oij, iboard, fn=check_cycle, *args, **kwargs):
    oi, oj = oij
    new_board = [l.copy() for l in iboard]
    new_board[oi][oj] = 1
    return fn(new_board, *args, **kwargs)

def part2(board, mp=True, visualize=False):
    obstacles = get_possible_obstacles([l.copy() for l in board])
    if mp:
        if visualize:
            raise ValueError("Cannot visualize with multiprocessing")

        from itertools import cycle
        from tqdm.contrib.concurrent import process_map

        return sum(process_map(inner, obstacles, cycle([board]), chunksize=5, leave=False))
    return sum(inner(o, board, animate=bool(visualize)) for o in obstacles)

# part2(parse_input("test"), False, True)
print(part2(parse_input("input")))
