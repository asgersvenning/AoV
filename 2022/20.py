import numpy as np

with open("input_20.txt", "r") as f:
    lines = f.readlines()
    
encrypted = [int(l.strip()) for l in lines]

# Test case
# encrypted = [1, 2, -3, 3, -2, 0, 4] 

def move_number(ind, number):
    ind = (ind + number) % (len(encrypted) - 1)
    return ind

def mixin(encrypted, order=False):
    indices = np.arange(len(encrypted)) 
    orderI = indices.copy() if type(order) == bool else order
    decrypted = [""] * len(encrypted)
    
    for ind in orderI:
        v, i, = encrypted[ind], indices[ind]
        j = move_number(i, v)
        
        if j > i: indices[np.logical_and(indices <= j, indices > i)] -= 1 
        if j < i: indices[np.logical_and(indices < i, indices >= j)] += 1 
        indices[ind] = j
        
        decrypted.pop(i)
        decrypted.insert(j, v)
    
    return decrypted, indices[orderI]

def getAnswer(encrypted):
    ind_0 = [i for i, v in enumerate(encrypted) if v == 0][0]
    
    return int(sum([encrypted[(ind_0 + i) % len(encrypted)] for i in [1000, 2000, 3000]])) 

# Part one

decrypted, _ = mixin(encrypted)
print("Part 1:", getAnswer(decrypted))

# Part two

mult = 811589153 
new_mult = mult % (len(encrypted) - 1)

encrypted = [i * new_mult for i in encrypted]

order = True
for i in range(10):
    decrypted, order = mixin(decrypted if i != 0 else encrypted, order=order)
    
print("Part 2:", getAnswer(decrypted) * mult // new_mult)