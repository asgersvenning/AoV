input_path = "input_02.txt"
with open(input_path, "r") as f:
    lines = [l.split(" ") for l in f.read().strip().split("\n")]
    

pretty_dict = {"R" : "Rock", "P" : "Paper", "S" : "Scissors"}
v = {"win" : 6, "draw" : 3, "loss" : 0, 
       "R" : 1,    "P" : 2,    "S" : 3}

# Part 1
d = {"A" : "R", "B" : "P", "C" : "S", 
     "X" : "R", "Y" : "P", "Z" : "S"}
outcome_dict = {"R" : {"R" : "draw", "P" : "loss", "S" : "win"},
                "P" : {"R" : "win", "P" : "draw", "S" : "loss"},
                "S" : {"R" : "loss", "P" : "win", "S" : "draw"}}

rounds = [[d[c] for c in l] for l in lines]
    
Answer_1 = sum([v[outcome_dict[r[1]][r[0]]] + v[r[1]] for r in rounds])
print("Part 1:", Answer_1)


# Part 2
state_dict = {"X" : "loss", "Y" : "draw", "Z" : "win"}
force_dict = {"win" : {"R" : "P", "P" : "S", "S" : "R"},
              "draw" : {"R" : "R", "P" : "P", "S" : "S"},
              "loss" : {"R" : "S", "P" : "R", "S" : "P"}}
    
Answer_2 = sum([v[state_dict[r[1]]] + v[force_dict[state_dict[r[1]]][d[r[0]]]] for r in lines])

print("Part 2:", Answer_2)

## Easy to read version of Part 1
# Answer_1 = 0

# for r in rounds:
#     result = outcome_dict[r[1]][r[0]]
#     choice = r[1]
#     result_cost = v[result]
#     choice_cost = v[choice]
#     Answer_1 += result_cost + choice_cost

## Easy to read version of Part 2
# Answer_2 = 0

# for r in lines:
#     result = state_dict[r[1]]
#     choice = force_dict[result][d[r[0]]]
#     result_cost = v[result]
#     choice_cost = v[choice]
#     Answer_2 += result_cost + choice_cost