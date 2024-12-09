def parse_input(path):
    rules, updates, isRule = [], [], True
    with open(path, "r") as f:
        [(rules if isRule else updates).append(list(map(int, line.split("|" if isRule else ",")))) for line in list(map(str.strip, f.readlines())) if line != "" or (isRule := not isRule)]
    return rules, updates

def ordering(before_after):
    rules, inv_rules = {}, {}
    [(lambda x, y : None)(rules.update({before : rules.get(before, []) + [after]}), inv_rules.update({after : inv_rules.get(after, []) + [before]})) for before, after in before_after]
    return rules, inv_rules

def part1(rules, updates):
    ao, bo = ordering(rules)
    middles = []
    for update in updates:
        valid = []
        for i in range(len(update)):
            b, v, a = update[:i], update[i], update[(i+1):]
            if any([bv in ao.get(v, []) for bv in b]) or any([av in bo.get(v, []) for av in a]):
                valid.append(False)
                break
            valid.append(True)
        middles.append(update[len(update) // 2] if all(valid) else 0)
    return sum(middles)
     
# print(part1(*parse_input("2024/inputs/05.test")))
print(part1(*parse_input("2024/inputs/05.input")))

def reorder(update : list[int], ao : dict, bo : dict):
    if len(update) <= 1:
        return update
    for i, e in enumerate(update):
        b, a = update[:i], update[(i+1):]
        ar, br = ao.get(e, []), bo.get(e, [])
        an, bn = [], []
        for ae in a.copy():
            if ae in br:
                a.remove(ae)
                bn.append(ae)
        for be in b.copy():
            if be in ar:
                b.remove(be)
                an.append(be)
        if an or bn:
            return reorder(b + bn, ao, bo) + [e] + reorder(an + a, ao, bo)
    return update

def part2(rules, updates):
    ao, bo = ordering(rules)
    middles = []
    for update in updates:
        sorted_update = reorder(update, ao, bo)
        if not all([i == j for i, j in zip(update, sorted_update)]):
            middles.append(sorted_update[len(sorted_update) // 2])
    return sum(middles)

# print(part2(*parse_input("2024/inputs/05.test")))
print(part2(*parse_input("2024/inputs/05.input")))