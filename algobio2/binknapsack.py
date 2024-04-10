#!/usr/bin/pypy3 # massive performance gain

class instance:
    # takes a max weight and a list of objects as (value, weight) tuples
    def __init__(self, weight, objects):
        self.weight = weight
        self.objects = objects

    def add(obj):
        self.objects += obj

# greedily solves a 01knapsack instance
def greedy(inst):
    sort = sorted(inst.objects, key= lambda x: x[0]/x[1], reverse=True)
    sol = []
    score = 0
    remweight = inst.weight
    while remweight > 0 and sort: # can still extend
        if sort[0][1] <= remweight: # if possible, extend
            sol.append(sort[0])
            score += sort[0][0]
            remweight -= sort[0][1]
        sort = sort[1:] # discard the element
    return (score, sol)

# determines the maximum greedy solution for a 01knapsack instance
def greedyscore(inst):
    sort = sorted(inst.objects, key=lambda x: x[0]/x[1], reverse=True)
    score = 0
    remweight = inst.weight
    while remweight > 0 and sort: # can still extend
        if sort[0][1] <= remweight: # if possible, extend
            score += sort[0][0]
            remweight -= sort[0][1]
        sort = sort[1:] # discard the element
    return score

# a Hirschberg-corrected DP approach to find the optimal solution to the 01knapsack instance
# has a runtime in O(weight*|objects|)
# only takes O(weight + |objects|) memory
def optimalscore(inst):
    # init arrays
    new = [0 for i in range(0, inst.weight +1)] # <= not <
    old = [0 for i in range(0, inst.weight +1)] # <= not <
    buf = old

    # iterate over objects
    for obj in inst.objects:
        # swap the arrays
        buf = old
        old = new
        new = buf
        for w in range(0, obj[1]): # copy over the not updatable cells
            new[w] = old[w]
        for w in range(obj[1], len(old)): # skip weights we could not reach; automatically skips 0
            new[w] = max(old[w-obj[1]] + obj[0], old[w])

    return max(new)

if __name__ == '__main__':
    import random as ran

    def bench(n, i):
        scores = []
        for l in range(0, 30):
            obj = [(ran.randint(1, 10), ran.randint(1, 10)) for i in range(0, i)]
            weight = n
            inst = instance(weight, obj)
            scores.append(greedyscore(inst)/optimalscore(inst))

        return sum(scores)/(len(scores))

    with open('./greedy.csv', 'w') as f:
        f.write("n, i, score\n")
        for reps in range(0, 10):
            for i in range(10, 150):
                for n in [1, 2, 3, 4, 5, 6, 7]:
                    f.write(f"{n},{i},{bench(n*i, i)}\n")
