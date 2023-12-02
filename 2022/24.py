import numpy as np
import sympy as sp

# input_board = "#.######\n#>>.<^<#\n#.<..<<#\n#>v.><>#\n#<^v^^>#\n######.#"

with open("input_24.txt", "r") as f:
    input_board = f.read().strip()

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

direction_dict = {"^" : "up", "v" : "down", "<" : "left", ">" : "right"}
inv_direction_dict = {v : k for k, v in direction_dict.items()}

class Blizzard:
    def __init__(self, x, y, dir, width, height):
        self.x = x
        self.y = y
        self.dir = direction_dict[dir]
        self.width = width
        self.height = height
        self.xmin = 0
        self.xmax = width - 1
        self.ymin = 0
        self.ymax = height - 1
        
    def move(self):
        x = self.x
        y = self.y
        if self.dir == "down":
            y += 1
        elif self.dir == "up":
            y -= 1
        elif self.dir == "left":
            x -= 1
        elif self.dir == "right":
            x += 1
        
        if x == self.xmax:
            x = self.xmin + 1
        elif x == self.xmin:
            x = self.xmax - 1
        elif y == self.ymax:
            y = self.ymin + 1
        elif y == self.ymin:
            y = self.ymax - 1
        return Blizzard(x, y, inv_direction_dict[self.dir], self.width, self.height)

def read_board(board):
    board = board.split("\n")
    board_height = len(board)
    board_width = len(board[0])
    exit = [[i for i, v in enumerate(board[-1]) if v == "."][0], len(board) - 1]
    assert type(exit[0]) == int, "Entrance not properly parsed"
    entrance = [[i for i, v in enumerate(board[0]) if v == "."][0], 0]
    assert type(entrance[0]) == int, "Exit not properly parsed"
    blizzards = []
    for y in range(board_height):
        for x in range(board_width):
            if board[y][x] in direction_dict:
                blizzards.append(Blizzard(x, y, board[y][x], board_width, board_height))
            elif board[y][x] == "E":
                raise ValueError("Player found in board")
            elif board[y][x] == "#" and not (x == 0 or x == board_width - 1 or y == 0 or y == board_height - 1):
                raise ValueError("Wall found inside board")
    return board_height, board_width, entrance, exit, blizzards
            
class Player:
    def __init__(self, entrance, exit, pos = None):
        if pos:
            self.x = pos[0]
            self.y = pos[1]
        else:
            self.x = entrance[0]
            self.y = entrance[1]
        self.goal = exit
        self.entrance = entrance
        
        self.xmin = 0
        self.xmax = board_width - 1
        self.ymin = 0
        self.ymax = board_height - 1
        
        self.exitReached = self.x == self.goal[0] and self.y == self.goal[1]
        self.valid = self.x > self.xmin and self.x < self.xmax and self.y > self.ymin and self.y < self.ymax or self.x == self.entrance[0] and self.y == self.entrance[1]
    
    def move(self, dir):
        y = self.y
        x = self.x
        if dir == "down":
            y += 1
        elif dir == "up":
            y -= 1
        elif dir == "left":
            x -= 1
        elif dir == "right":
            x += 1
        elif dir == "stay":
            pass
        
        return Player(self.entrance, self.goal, [x, y])
    
def board_positions(blizzards):
    board = np.zeros((board_height, board_width), dtype=np.int32)
    board[[b.y for b in blizzards], [b.x for b in blizzards]] += 1
    return board
            
def draw_board(blizzards, player, i):
    board = []
    for y in range(board_height):
        row = []
        for x in range(board_width):
            if y == 0 and x == (board_width - 1):
                row.append(color.BOLD + color.YELLOW + str(i) + color.END)
                continue
            this_blizzards = [b for b in blizzards if x == b.x and y == b.y]
            entrance_or_exit = False
            
            if x == 0 or x == board_width - 1 or y == 0 or y == board_height - 1:
                if this_blizzards:
                    raise ValueError("Blizzard found on board edge")
                elif [x, y] == entrance:
                    row.append(".")
                    entrance_or_exit = True
                elif [x, y] == exit:
                    row.append(".")
                    entrance_or_exit = True
                else:
                    row.append("#")
                    continue
            
            if x == player.x and y == player.y:
                if entrance_or_exit:
                    row.pop()
                if len(this_blizzards) != 0:
                    row.append(color.RED + color.BOLD + "X" + color.END)
                    Warning("Player found on blizzard")
                else:
                    row.append(color.GREEN + color.BOLD + "E" + color.END)
                continue
            
            if entrance_or_exit:
                continue
            
            if len(this_blizzards) == 1:
                row.append(color.BLUE + color.BOLD + inv_direction_dict[this_blizzards[0].dir] + color.END)
            elif len(this_blizzards) > 1:
                row.append(color.BLUE + color.BOLD + str(len(this_blizzards)) + color.END)
            else:
                row.append(".")
        board.append("".join(row))
    print("\n".join(board))

board_height, board_width, entrance, exit, init_blizzards = read_board(input_board)

wrapMult = (board_width - 2) * (board_height - 2)
print("Max wrapMult", wrapMult)
for p in range(1, wrapMult):
    if (p % (board_width - 2)) == 0 and (p % (board_height - 2)) == 0:
        wrapMult = p
        break
print("Board dimensions", board_height, board_width)
print("Best wrapMult", wrapMult)

board_dict = np.zeros((wrapMult, board_height, board_width), dtype=np.int32) - 1
blizzard_dict = np.zeros((wrapMult, board_height, board_width), dtype=np.int32)
blizzards = init_blizzards
for i in range(wrapMult):
    blizzard_dict[i] = board_positions(blizzards)
    blizzards = [b.move() for b in blizzards]
print("Precompute finished!")
nextcall = [[Player(entrance, exit), 0, dir] for dir in ["up", "down", "left", "right", "stay" ]]

def next_to_call(v):
    return v[0].move(v[2]), v[1]

def split_player(player, i):
    ind = i % wrapMult
    blizzard_pos = blizzard_dict[ind]
    
    if player.exitReached:
        return i
    if not player.valid or blizzard_pos[player.y, player.x] != 0:
        return

    v = board_dict[ind, player.y, player.x]
    if v == -1:
        board_dict[ind, player.y, player.x] = i
    elif v <= i:
        return 
    else:
        board_dict[ind, player.y, player.x] = i
    
    for dir in ["up", "left", "down", "right", "stay"]:
        nextcall.append([player, i + 1, dir])

while True:
    # print(len(nextcall))
    minMoves = split_player(*next_to_call(nextcall.pop(0)))
    if minMoves:
        break

print("Part 1:", minMoves)

entrance, exit = exit, entrance
nextcall = [[Player(entrance, exit).move(dir), minMoves + 1, dir] for dir in ["up", "down", "left", "right", "stay" ]]

while True:
    minMoves = split_player(*next_to_call(nextcall.pop(0)))
    if minMoves:
        break

entrance, exit = exit, entrance
nextcall = [[Player(entrance, exit).move(dir), minMoves + 1, dir] for dir in ["up", "down", "left", "right", "stay" ]]

while True:
    minMoves = split_player(*next_to_call(nextcall.pop(0)))
    if minMoves:
        break

print("Part 2:", minMoves)