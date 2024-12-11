from helpers import get_lines, get_path

def parse_input(type : str):
    return list(map(int, get_lines(get_path(type))[0].split(" ")))

def split(num : int):
    num = str(num)
    return int(num[:(half := len(num) // 2)]), int(num[half:])

def transmute(num : int):
    if num == 0:
        return (1, )
    if len(str(num)) % 2 == 0:
        return split(num)
    return (num * 2024, )

def blink(sequence : list[int]):
    return [new for stone in sequence for new in transmute(stone)]

def part1(sequence : list[int], n : int=25):
    if n == 1:
        return len(blink(sequence))
    return len([sequence := blink(sequence) for i in range(n)][-1])

print(part1(parse_input("test")))
# print(part1(parse_input("input")))

cache = []

def blink1_many(stone : int, n : int):
    global cache
    if n == 0:
        return 1
    while n >= len(cache):
        cache += [{}]    
    if not stone in cache[n]:
        cache[n][stone] = sum(blink1_many(new, n - 1) for new in transmute(stone))
    return cache[n][stone]

def part2(sequence : list[int], n : int=75):
    return sum(blink1_many(stone, n) for stone in sequence)

# print(part2(parse_input("test"), 25))
print(part2(parse_input("input"), 75))