from util_print import print_compact

BROKEN_LINKS = set([])
TIME = 0

def setup():
    """
    make initial setup of the network by creating:
    - adjacency matrix
    - next vectors
    - distance vectors
    """
    global BROKEN_LINKS
    BROKEN_LINKS = set([])

    # distance vectors for each router
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
    
    # next vectors to store the next address where to hop
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
    
    # adjacency matrix for the graph (network)
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

    # node is the vertex that shares its distance vectors
    for node in range(len(adj)):
        # neighbor is a vertex that is neighbor of the node
        for neighbor in [(node + 1) % len(adj), (node - 1) % len(adj)]:
            
            # if the link no longer exists
            if ((neighbor, node) in BROKEN_LINKS or (node, neighbor) in BROKEN_LINKS):
                continue

            # index is a vertex such that we update distance from the neighbor to index
            for index in range(len(adj)):

                prev = distance_vectors[neighbor][index]
                poss = adj[neighbor][node] + distance_vectors[node][index]

                # split horizon
                if (next_vectors[node][index] == neighbor):
                    continue

                # update path if the previous optimal path is from this node only
                if (next_vectors[neighbor][index] == node and distance_vectors[neighbor][index] != poss):
                    distance_vectors[neighbor][index] = poss
                    updated = True
                    continue

                # if better path is discovered
                if (poss < prev):
                    distance_vectors[neighbor][index] = poss
                    next_vectors[neighbor][index] = node
                    updated = True

    return distance_vectors, next_vectors, updated

def break_link(adj, distance_vectors, next_vectors, node1 = 1, node2 = 2):
    global BROKEN_LINKS

    # add the broken link into BROKEN_LINKS set
    BROKEN_LINKS.add((node1, node2))
    
    for i in range(len(adj)):
        for j in [node1, node2]:
            # reset to infinity in all cases where path
            # contained link that is know broken
            if (next_vectors[j][i] == node1 + node2 - j):
                distance_vectors[j][i] = float('inf')
                next_vectors[j][i] = None
                adj[j][i] = float('inf')

    return adj, distance_vectors, next_vectors

def run_until_stable(adj, distance_vectors, next_vectors, print_func = print_compact):
    global TIME

    while (True):
        distance_vectors, next_vectors, updated = update(adj, distance_vectors, next_vectors)

        # check if any update occurred to stop
        if (not updated):
            return distance_vectors, next_vectors

        print(f"At time = {TIME}")
        print_func(distance_vectors, next_vectors)
        print()
        
        TIME += 1

    return distance_vectors, next_vectors

def run_program(print_func = print_compact):
    print()
    global TIME

    # setup
    adj, distance_vectors, next_vectors = setup()
    
    print(f"At time = {TIME}")
    print_func(distance_vectors, next_vectors)
    print()
    TIME += 1

    # run DVR algorithm until routing tables become stable
    distance_vectors, next_vectors = run_until_stable(adj, distance_vectors, next_vectors, print_func)
    
    print(f"At time = {TIME}")
    print_func(distance_vectors, next_vectors)
    print()
    TIME += 1
    print("Stable...\nLink Broken!\n\n")

    # break the link at stability
    adj, distance_vectors, next_vectors = break_link(adj, distance_vectors, next_vectors)
    print(f"At time = {TIME}")
    print_func(distance_vectors, next_vectors)
    print()
    TIME += 1

    # run DVR algorithm until stable again
    distance_vectors, next_vectors = run_until_stable(adj, distance_vectors, next_vectors, print_func)

    print("\nStable...\n")

# run the program
run_program()