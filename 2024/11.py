from helpers import get_lines, get_path

def parse_input(type : str):
    return list(map(int, get_lines(get_path(type))[0].split(" ")))

def split(num : int):
    return (int(num[:(half := len(num) // 2)]), int(num[half:])) if (num := str(num)) else (-1, -1)

def transmute(num : int):
    return (1, ) if num == 0 else split(num) if len(str(num)) % 2 == 0 else (num * 2024, )

def blink(sequence : list[int]):
    return [new for stone in sequence for new in transmute(stone)]

def part1(sequence : list[int], n : int=25):
    return len([sequence := blink(sequence) for _ in range(n)][-1]) if n > 1 else len(blink(sequence))

print(part1(parse_input("test")))
# print(part1(parse_input("input")))

cache = {}

def update_cache(stone : int, n : int):
    global cache
    if n not in cache:
        cache[n] = {}
    if stone not in cache[n]:
        cache[n][stone] = sum(blink1_many(new, n - 1) for new in transmute(stone))

def blink1_many(stone : int, n : int):
    return 1 if n == 0 or not update_cache(stone, n) is None else cache[n][stone]

def part2(sequence : list[int], n : int=75):
    return sum(blink1_many(stone, n) for stone in sequence)

# print(part2(parse_input("test"), 25))
print(part2(parse_input("input"), 75))

# import sys
# sys.setrecursionlimit(1000000)
# blink1000 = part2(parse_input("input"), 1000)
# print(len(str(blink1000)), blink1000)