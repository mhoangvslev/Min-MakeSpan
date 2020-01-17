import numpy as np

def getTokenIfValid(seq: str):
    """Parse l'entrée et transforme en array"""
    tokens = seq.split(":")
    m, n, tasks = int(tokens[0]), int(tokens[1]), tokens[2:len(tokens)]
    if(n != len(tasks)):
        print("Il n'y a pas assez de tâches, il en faut n(", n, ")")
        return None

    return tokens

def main():
    canStart = False
    mode = -1
    while(not canStart):
        mode = -1
        while(mode not in range(4)):
            print("Choisissez le mode: 0 - fichier, 1 - clavier, 2 - I_m, 3 - I_R")
            mode = int(input())
        
        # Mode I_f
        if(mode == 0):
            print("Saisissez le nom du fichier")
            file = open(input(), "r")
            instance = getTokenIfValid(file.readline())
            file.close()
            canStart = True
        
        # Mode I_c
        elif(mode == 1):
            print("Saisissez la séquence m:n:d1:d2:...:dn")
            instance = getTokenIfValid(input())
            canStart = True

        # Mode I_m
        elif(mode == 2):
            print("Saisissez m: ")
            m = int(input())
            tasks = np.concatenate((
               [m for i in range(3)],
               np.repeat([m + i for i in range(1, m)], 2)
            ))

            print(tasks)
            instance = np.concatenate(([m, len(tasks)], tasks))
            canStart = True
        
        # Mode I_R
        elif(mode == 3):
            instances = []
            print("Saisissez n, m, k, min, max. Par exemple: 'n m k min max'")
            n, m, k, low, high = [int(item) for item in input().split()]
            print(n, m, k, low, high)
            for i in range(k):
                instances.append(
                    np.concatenate(([m, n], np.random.randint(low, high+1, size=n)))
                )
                            
            canStart = True


    if(mode != 3):
        m, n, tasks = int(instance[0]), int(instance[1]), [int(task) for task in instance[2:len(instance)]]
        print("Borne inférieure \"maximum\" = ", max(tasks))
        print("Borne inférieure \"moyenne\" = ", sum(tasks)/m)

        # LSA
        lsa_sol = LSA(m, tasks)
        lsa_load = dict(map(lambda item: (item[0], sum(item[1])), lsa_sol.items())) 
        lsa_mes = max(lsa_load.values())
        print("Résultat LSA = ", lsa_sol, " measure: ", lsa_mes)
        print("Ratio LSA = ", round(lsa_mes/(sum(tasks)/m), 3))

        # LPT
        lpt_sol = LPT(m, tasks)
        lpt_load = dict(map(lambda item: (item[0], sum(item[1])), lpt_sol.items())) 
        lpt_mes = max(lpt_load.values())
        print("Résultat LPT = ", lpt_sol, " measure: ", lpt_mes)
        print("Ratio LPT = ", round(lpt_mes/(sum(tasks)/m), 3))

        # MyAlgo
        myalgo_sol = LPT(m, tasks)
        myalgo_load = dict(map(lambda item: (item[0], sum(item[1])), myalgo_sol.items())) 
        myalgo_mes = max(myalgo_load.values())
        print("Résultat MyAlgo = ", myalgo_sol, " measure: ", myalgo_mes)
        print("Ratio MyAlgo = ", round(myalgo_mes/(sum(tasks)/m), 3))
    else:
        lsa_mes, lpt_mes, myalgo_mes = [], [], []
        for instance in instances:
            m, n, tasks = int(instance[0]), int(instance[1]), [int(task) for task in instance[2:len(instance)]]
            
            # LSA
            lsa_sol = LSA(m, tasks)
            lsa_mes.append(
                max(dict(
                    map(
                        lambda item: (item[0], 
                        sum(item[1])), lsa_sol.items()
                    )
                ).values())/(sum(tasks)/m)
            )

            # LPT
            lpt_sol = LPT(m, tasks)
            lpt_mes.append(
                max(dict(
                    map(
                        lambda item: (item[0], 
                        sum(item[1])), lpt_sol.items()
                    )
                ).values())/(sum(tasks)/m)
            )

            # MyAlgo
            myalgo_sol = LSA(m, tasks)
            myalgo_mes.append(
                max(dict(
                    map(
                        lambda item: (item[0], 
                        sum(item[1])), myalgo_sol.items()
                    )
                ).values())/(sum(tasks)/m)
            )
        
        print("ratio moyen LSA =", round(np.mean(lsa_mes), 3))
        print("ratio moyen LPT =", round(np.mean(lpt_mes), 3))
        print("ratio moyen MyAlgo =", round(np.mean(myalgo_mes), 3))

def LSA(m: int, tasks: list):
    """Les tâches seront traités dans l'ordre tel qu'elles sont fournies"""

    M = dict([(i, []) for i in range(1, m+1)])
    
    for task in tasks:
        availIdx = 1
        loads = dict(map(lambda item: (item[0], sum(item[1])), M.items())) 
        availIdx = min(loads, key=loads.get)
        M[availIdx].append(task)
    
    return M

def LPT(m: int, tasks: list):
    """Les tâches seront traités dans l'ordre décroissant de leur durée"""

    M = dict([(i, []) for i in range(1, m+1)])
    tasks = np.sort(tasks, kind="mergesort")[::-1] # Trier selon l'ordre décroissant, O(n*log(n)) mergesort 
    #tasks = np.sort(tasks)[::-1] # O(n^2) quicksort par défaut
    
    for task in tasks:
        availIdx = 1
        loads = dict(map(lambda item: (item[0], sum(item[1])), M.items())) 
        availIdx = min(loads, key=loads.get)
        M[availIdx].append(task)
    
    return M

def MyAlgo(m: int, tasks: list):
    """Affecter les tâches en utilisant le principe du Min Binpacking. On va essayer de faire m bins de capacité ~opt """

    M = dict([(i, []) for i in range(1, m+1)])
    opt = np.ceil(len(tasks)/m)
    tasks = tasks = np.sort(tasks, kind="mergesort")
    
    # 
    macIdx = 1
    for task in tasks:
        if(macIdx < m - 1):
            while(sum(M[macIdx]) <= opt):
                M[macIdx].append(task)
            macIdx += 1
        else:
            M[macIdx].append(task)
    
    return M

main()