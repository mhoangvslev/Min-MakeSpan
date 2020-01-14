
def isValid(seq: string):
    tokens = seq.split(":")

    if(len(tokens) <= 2):
        file = open(seq, "r")
        tokens = file.readline().split(":")
        if(len(tokens) <= 2):
            return None

    m, n = tokens[0], tokens[1]
    if(n != len(tokens[2:len(tokens)])):
        print("Il n'y a pas assez de tâches, il en faut n(", n, ")")
        return None

    return tokens

def main():
    tokens = None
    while(tokens != None):
        print("Enter fileName.txt or the sequence")
        stdin = input()
        tokens = isValid(stdin)
    
    m, n = int(tokens[0]), int(tokens[1])
    tasks = tokens[2:len(tokens)]

def LSA(m: int, n: int, tasks):
    M = dict()
    for i in range(1, m+1):
        M[i] = []
    
    for task in tasks:
        availIdx = 1
        for macIdx in M.keys():
            if len(M[macIdx]) == 0: # Free machine
                availIdx = macIdx
                break
            elif M[macIdx][-1] < task and M[macIdx][-1] < M[availIdx][-1]:
                availIdx = macIdx
        M[availIdx].append(task)
    
    return M