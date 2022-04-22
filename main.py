from util_print import print_compact, print_matrices, print_matrix

BROKEN_LINKS = set([])
TIME = 0

def setup():
    global BROKEN_LINKS
    BROKEN_LINKS = set([])

    distance_vectors = [
        [
            1 if j in [(i+1)%5, (i-1)%5]
            else (
                0 if (i == j)
                else float('inf')
            )
            for j in range(5)
        ]
        for i in range(5)
    ]
    
    next_vectors = [
        [
            j if j in [(i+1)%5, (i-1)%5]
            else (
                i if (i == j)
                else None
            )
            for j in range(5)
        ]
        for i in range(5)
    ]
    
    adj = [
        [
            1 if j in [(i+1)%5, (i-1)%5]
            else (
                0 if (i == j)
                else float('inf')
            )
            for j in range(5)
        ]
        for i in range(5)
    ]
    return adj, distance_vectors, next_vectors

def update(adj, distance_vectors, next_vectors):
    """
    Run one round of updates.
    """

    global BROKEN_LINKS

    updated = False

    for node in range(5): # node is the vertex that shares its distance vectors
        for neighbor in [(node + 1) % 5, (node - 1) % 5]: # neighbor is a vertex that is neighbor of the node
            
            if ((neighbor, node) in BROKEN_LINKS or (node, neighbor) in BROKEN_LINKS): # if the link no longer exists
                continue

            for index in range(5): # index is a vertex such that we update distance from the neighbor to index

                prev = distance_vectors[neighbor][index]
                poss = adj[neighbor][node] + distance_vectors[node][index]

                if (next_vectors[node][index] == neighbor): # split horizon
                    continue

                if (next_vectors[neighbor][index] == node and distance_vectors[neighbor][index] != poss): # update path if the previous optimal path is from this node only
                    distance_vectors[neighbor][index] = poss
                    updated = True
                    continue

                if (poss < prev): # if better path is discovered
                    distance_vectors[neighbor][index] = poss
                    next_vectors[neighbor][index] = node
                    updated = True

    return distance_vectors, next_vectors, updated

def break_link(adj, distance_vectors, next_vectors, node1 = 1, node2 = 2):
    global BROKEN_LINKS

    BROKEN_LINKS.add((node1, node2))
    
    for i in range(5):
        for j in [node1, node2]:
            if (next_vectors[j][i] == node1 + node2 - j):
                distance_vectors[j][i] = float('inf')
                next_vectors[j][i] = None
                adj[j][i] = float('inf')

    return adj, distance_vectors, next_vectors

def run_until_stable(adj, distance_vectors, next_vectors, print_func = print_compact):
    global TIME

    while (True):
        distance_vectors, next_vectors, updated = update(adj, distance_vectors, next_vectors)

        if (not updated):
            return distance_vectors, next_vectors

        print(f"At time = {TIME}")
        print_func(distance_vectors, next_vectors)
        print()
        
        TIME += 1

    return distance_vectors, next_vectors

def run_program(print_func = print_compact):
    global TIME

    adj, distance_vectors, next_vectors = setup()
    
    print(f"At time = {TIME}")
    print_func(distance_vectors, next_vectors)
    print()
    TIME += 1

    distance_vectors, next_vectors = run_until_stable(adj, distance_vectors, next_vectors, print_func)
    
    print("\nStable...\nLink Broken!\n")

    adj, distance_vectors, next_vectors = break_link(adj, distance_vectors, next_vectors)
    print(f"At time = {TIME}")
    print_func(distance_vectors, next_vectors)
    print()
    TIME += 1


    distance_vectors, next_vectors = run_until_stable(adj, distance_vectors, next_vectors, print_func)

    print("\nStable...\n")

run_program()