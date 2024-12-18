import numpy as np
from tqdm import tqdm

from helpers import Animation, from_import, get_lines, get_path

from_import("16", ["State", "PriorityQueue", "update", "render_history", "backtrace"])

def parse_input(type : str):
    return (list(reversed(list(map(int, line.split(","))))) for line in get_lines(get_path(type)))

def shortest_path(maze : np.ndarray, animate : bool=False, verbose : bool=False):
    start = (0, 0)
    end = tuple(s - 1 for s in maze.shape)
    queue = PriorityQueue([State(*start, 0, (0, 1), 0)])
    
    anim = Animation()
    while queue and maze[*end] == -1:
        update(maze, queue)
        if animate:
            anim += render_history(maze, queue.history(), start, end)

    best_path = backtrace(queue.history(), start)
    if verbose or animate:
        last_frame = render_history(maze, best_path, start, end)
        last_frame += f'\n{f'Total = {best_path[0].total}':^{maze.shape[1]}}'
        if animate:
            anim += last_frame
            anim(4 / len(anim), transient=False)
        elif verbose:
            Animation([last_frame])(0, transient=False)
    return best_path[0]

def part1(type : str, size : tuple[int, int]=(70, 70), age : int=1024, animate : bool=False, verbose : bool=False):
    memory = -np.ones(tuple(s + 1 for s in size))
    bytes = parse_input(type)
    for i, byte in enumerate(bytes):
        if i >= age:
            break
        memory[*byte] = 0
    return shortest_path(memory, animate, verbose)

# part1("test", (6, 6), 12, True)
print(part1("input").total)
# print(*parse_input("test"))

def part2(type : str, size : tuple[int, int]=(70, 70), visualize : bool=False):
    bytes = get_lines(get_path(type))
    max_possible_age = min((i for i, byte in enumerate(bytes) if byte == ",".join(map(str, size))), default=len(bytes))
    age = 0
    pbar = tqdm(reversed(range(max_possible_age)), leave=False)
    for age in pbar:
        end = part1(type, size, age)
        pbar.set_description(str(end))
        if end == size:
            break
    if visualize:
        print(f"Before {bytes[age]}:")
        part1(type, size, age, False, True)
        print(f"\nAfter {bytes[age]}:")
        part1(type, size, age+1, False, True)
    return bytes[age]

# print(part2("test", (6, 6), True))
print(part2("input"))