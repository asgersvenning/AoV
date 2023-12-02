import re

class Game:
    def __init__(self, input):
        game, parts = input.split(": ")
        shows = parts.split("; ")

        self.number = int(re.search("(?<=^Game )\d+(?=$)", game).group(0))
        self.shows = [Show(show) for show in shows]
    
    def __str__(self):
        repr_str = f'Game {self.number:0>4}:   Red Green Blue\n'
        for si, show in enumerate(self.shows):
            repr_str += f'  Show {si:0>4}: {show.red: ^3} {show.green: ^5} {show.blue: ^4}\n' 
        return repr_str
    
    def __repr__(self):
        return str(self)

class Show:
    def __init__(self, show_str : str):
        cubes = show_str.strip().split(", ")
        self.counts = {
            "red" : 0,
            "green" : 0,
            "blue" : 0
        }
        for cube in cubes:
            count, color = cube.split(" ")
            self.counts[color] = int(count)

    @property
    def red(self, value):
        self.counts["red"] = value
    @property
    def green(self, value):
        self.counts["green"] = value
    @property
    def blue(self, value):
        self.counts["blue"] = value

    @red.getter
    def red(self):
        return self.counts["red"]
    @green.getter
    def green(self):
        return self.counts["green"]
    @blue.getter
    def blue(self):
        return self.counts["blue"]
    

path = "inputs/02.input"
max_possible = {
    "red" : 12,
    "green" : 13,
    "blue" : 14
}
total_sum = 0

def game_is_possible(game : "Game") -> bool:
    for show in game.shows:
        for color in ["red", "green", "blue"]:
            if show.counts[color] > max_possible[color]:
                return False
    return True

with open(path, "r") as file:
    for line in file.readlines():
        this_game = Game(line)
        if game_is_possible(this_game):
            total_sum += this_game.number

print(total_sum)

# Part 2

total_sum = 0

from typing import List
from math import prod

def minimum_set(game : "Game") -> List[int]:
    sets = {
        "red" : [],
        "green" : [],
        "blue" : []
    }
    for show in game.shows:
        for color, count in show.counts.items():
            sets[color].append(count)

    return [max(i) for _, i in sets.items()]

with open(path, "r") as file:
    for line in file.readlines():
        this_game = Game(line)
        mset = minimum_set(this_game)
        pow = prod(mset)
        total_sum += pow

print(total_sum)