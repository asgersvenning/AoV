import re

digit_dict = {
    "zero" : "0",
    "one" : "1",
    "two" : "2",
    "three" : "3",
    "four" : "4",
    "five" : "5",
    "six" : "6",
    "seven" : "7",
    "eight" : "8",
    "nine" : "9"
}
# digit_dict = {}
correct_digits = [str(i) for i in range(10)]

def get_first_and_last(s):
    digits = re.findall(r'(?=(\d|zero|one|two|three|four|five|six|seven|eight|nine))', s)
    digits = [digit_dict[digit] if digit in digit_dict else digit for digit in digits]
    digits = [digit for digit in digits if digit in correct_digits]
    return digits[0], digits[-1]

path = "inputs/01.input"
total_sum = 0

with open(path, "r") as f:
    for line in f.readlines():
        first, last = get_first_and_last(line)
        total_sum += int(f'{first}{last}')

print(total_sum)
