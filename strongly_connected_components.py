import file_IO_helper as fio

def bin_search(needle, haystack):
    '''Run of the mill binary search. Assumes haystack is sorted from low to high.
    '''
    low = 0
    high = len(haystack) - 1
    mid = 0
    while low <= high: 
        mid = (high + low) // 2 
        if needle > haystack[mid]:      # ignore lower half
            low = mid + 1
        elif needle < haystack[mid]:    # ignore upper half
            high = mid - 1
        else:                           # found it!
            return mid 
    return None                         # needle not in haystack

def search_scc(needle, haystack):
    '''Searched a dict of lists (namely, strongly connected components) linearly to find
    the needle.
    '''
    for key in haystack:
        if needle in haystack[key]:
            return True
    return False

def partition_states(folder = "states"):
    '''This partitions all of the states (already generated) by the number of edges/nodes.
    The partitioning is done by a dictionary, where the key is the number of edges and the
    value is a list of the indices to the corresponding graphs.
    '''
    partition = {}
    i = 0
    while fio.graph_file(i, folder) != fio.next_graph(folder):
        graph = fio.read_graph(i, folder)
        try:
            partition[len(graph.nodes)].append(i)
        except:
            partition[len(graph.nodes)] = [i]
        i += 1
    return partition

def partition_class_to_matrix(part_class, folder = "states"):
    '''Given a list representing a part of a partition of states, this function creates an
    adjacency matrix for the provided states. (That is, the matrix returned is essentially
    the adjacency matrix of all of the states with the rows and columns pertaining to the
    states not listed removed.
    '''
    n = len(part_class)
    matrix = [[0 for i in range(n)] for j in range(n)] # make an nxn matrix of 0s
    row = 0
    while row < n:
        graph = fio.read_graph(part_class[row], folder)
        for out in graph.can_get_to:
            col = bin_search(out[2], part_class)
            if col is not None:  # if the outneighbour is in the partition
                matrix[row][col] = 1
        row += 1
    return matrix

def scc_dict_to_states_list(scc, part_class):
    scc_list = []
    for key in scc:
        component = []
        for i in scc[key]:
            component.append(part_class[i])
        scc_list.append(component)
    return scc_list

def visit(state, visited, matrix, order):
    '''Part of Kosaraju's algorithm.'''
    if not visited[state]:
        visited[state] = True
        col = 0
        while col < len(matrix[state]):
            if matrix[state][col] == 1:        # out-neighbour
                visit(col, visited, matrix, order)
            col += 1
        order.insert(0, state)

def assign(state, root, scc, matrix):
    '''Part of Kosaraju's algorithm.'''
    if not search_scc(state, scc):
        try:        # append it to the list
            scc[root].append(state)
        except:     # if there isn't a list, make one
            scc[root] = [state]
        row = 0
        while row < len(matrix):
            if matrix[row][state] == 1: # in neighbour
                assign(row, root, scc, matrix)
            row += 1

def partition_part_scc(part_class, folder = "states"):
    '''Given a list representing a part of a partition of states, this function finds the
    strongly connected components via Kosaraju's algorithm.
    '''
    matrix = partition_class_to_matrix(part_class, folder)
    visited = [False for i in range(len(part_class))]
    order = []
    scc = {}
    state = 0
    while state < len(part_class):
        visit(state, visited, matrix, order)
        state += 1
    state = 0
    while state < len(order):
        assign(state, state, scc, matrix)
        state += 1
    return scc_dict_to_states_list(scc, part_class)

def partitioned_get_scc(partition):
    '''Giving a partitioned automata of the states, returns the strongly connected
    components.
    '''
    scc = []
    for key in partition:
        part_scc = partition_part_scc(partition[key])
        scc.extend(part_scc)
    return scc

if __name__ == "__main__":
##    part = partition_states()
##    scc = partitioned_get_scc(part)
##    for elem in scc:
##        print(elem)
##        print()

    # Try for graphs from ic and triangle
    part = partition_states("states_from_tri_and_ic")
    scc = partition_part_scc(part[5], "states_from_tri_and_ic")
    for elem in scc:
        print(elem)
        print()
