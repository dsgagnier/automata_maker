'''While called adj_matrices, this module deals in particular with the functionality needed
to deal with the adjacency matrices of the graphs that are being folded (ie not of the
adjacency matrices of the automata. For functionality to do with the latter, see the file
strongly_connected_components.py
'''

import itertools

def make_matrix(size):
    '''This function makes a 3-D matrix such that the size of it is size x size x 3. The
    matrix is populated with 0s.
    '''
    return [[[0 for i in range(3)] for j in range(size)] for k in range(size)]

def print_m(matrix):
    '''Prints a matrix more nicely.'''
    for row in matrix:
        print(row)
    print()

def is_symmetric(matrix):
    '''Given a square matrix, indicates whether or not it is symmetric.'''
    for i in range(len(matrix)):
        for j in range(i,len(matrix)):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

def int_list(n):
    '''Makes a list where the entries are 0, 1, ... , n-1 '''
    int_list = []
    i = 0
    while i < n:
        int_list.append(i)
        i += 1
    return int_list

def get_combs(string):
    '''Given a string or list, returns all possible combinations of its characters as
    a list of tuples.
    '''
    combs = []
    i = 0
    while i <= len(string):
        new = list(itertools.combinations(string, i))
        combs.extend(new)
        i += 1
    return combs

def get_perms(a_list):
    '''Given a list, returns all possible permutations of its entries as a list of tuples.
    '''
    return list(itertools.permutations(a_list))

def permute_blocks(a_list, perm):
    '''Given a list of size 2n and a permutation of n elements, this function applies the
    permutation in the list, considering each element that's permtuted to be two adjacent
    elements in the list. For example:
    ['a','b','c','e','f','g'], [0,2,1] -> ['a','b','f','g','c','e']
    '''
    new = []
    for i in range(len(perm)):
        to_add = [a_list[2*perm[i]], a_list[2*perm[i] + 1]]
        new.extend(to_add)
        i += 1
    return new

def switch_blocks(a_list, comb):
    '''Given a list of size 2n and a combination of n elements, this function treats a_list
    as if it is n groups of 2 elements and swaps the order of the elements in the groups
    chosen by the permutation. For example:
    ['a','b','c','d','e','f'], [0, 2] -> ['b','a','c','d','f','e']
    '''
    new = a_list[:]
    i = 0
    while i < len(a_list)//2:
        if i in comb:
            new[2*i], new[2*i + 1] = new[2*i + 1], new[2*i] # swap!
        i += 1
    return new

def block_permutations(n):
    '''Given an even integer n, this function returns a list of all possible "block
    permutations." That is, permutations where the list of integers [1,2,...,n] is divided
    into groups of two ( [1,2, 3,4, ... , n-1,n] ) and then these blocks of two may be
    permuted, and the numbers within the blocks may be permuted.
    '''
    block_perms = []
    ints = int_list(n)
    half_ints = int_list(n//2)
    combs = get_combs(half_ints)
    perms = get_perms(half_ints)
    for comb in combs:
        new_one = switch_blocks(ints, comb)
        for perm in perms:
            new_two = permute_blocks(new_one, perm)
            block_perms.append(new_two)
    return block_perms
    

def permute_list(a_list, perm):
    '''Given a list and a permutation, applies the permutation to the list. For example,
    ['a','b','c','d'], [0,2,3,1] -> ['a','c','d','b']
    '''
    new = []
    for i in range(len(a_list)):
        new.append(a_list[perm[i]])
        i += 1
    return new

def symmetric_permute(matrix, perm):
    '''Given a 2-D matrix, applies a permutation to its rows and its columns'''
    matrix = permute_list(matrix, perm) #permute the rows
    for i in range(len(matrix)):
        matrix[i] = permute_list(matrix[i], perm)
    return matrix

def nodes_to_matrix(nodes):
    '''Given a list of nodes of a graph, this function makes an adjancency-like matrix.
    Each entry of a 2n x 2n matrix (where n is the number of edges/nodes) is a triple. Each
    row/column corresponds to the head or the tail of an edge. In the triple, the first
    entry is a 1 is the node heads/tails touch in the graph, the second entry is a 1 if
    the path on the graph goes over the intersection of the heads/tails, and the third
    entry is a 1 if the two node heads/tails form a head-tail pair.
    '''
    order = []
    matrix = make_matrix(len(nodes)*2)

    for i in range(len(nodes)):
        order.append(nodes[i].name + "h")
        order.append(nodes[i].name + "t")
        # Indicate all head-tail pairs:
        matrix[2*i][2*i + 1][2] = 1
        matrix[2*i + 1][2*i][2] = 1

    for node in nodes:
        for connected in node.head:
            row = order.index(node.name + "h")
            col = order.index(connected[0] + connected[1])
            # Set the first entry of the triple to 1
            matrix[row][col][0] = 1
            matrix[col][row][0] = 1
            if connected[2]:        # If the path goes over the turn
                matrix[row][col][1] = 1
                matrix[col][row][1] = 1

        for connected in node.tail:
            row = order.index(node.name + "t")
            col = order.index(connected[0] + connected[1])
            # Set the first entry of the triple to 1
            matrix[row][col][0] = 1
            matrix[col][row][0] = 1
            if connected[2]:        # If the path goes over the turn
                matrix[row][col][1] = 1
                matrix[col][row][1] = 1
    return matrix

def OLD_are_equal_adj(matrix1, matrix2):
    '''This function checks if two matrices are equal up to "symmetric permutation."
    This function is no longer to be used, but it here to reference if necessary.
    '''
    if len(matrix1) != len(matrix2):
        return False
    n = len(matrix1)
    perms = list(itertools.permutations(int_list(n)))
    for perm in perms:
        if symmetric_permute(matrix1, perm) == matrix2:
            return True
    return False

def are_equal_adj(matrix1, matrix2):
    if len(matrix1) != len(matrix2):
        return False
    n = len(matrix1)
    perms = block_permutations(n)
    for perm in perms:
        if symmetric_permute(matrix1, perm) == matrix2:
            return True
    return False

if __name__ == "__main__":
    import file_IO_helper as fio

    #check make_matrix
    test_matrix = make_matrix(4)
    print_m(test_matrix)

    #check nodes_to_matrix
    # Now out of date, but function should still work
##    graphs = fio.read_file("graphs")
##    test_matrix = nodes_to_matrix(graphs[0].nodes)
##    print_m(test_matrix)
##    print(is_symmetric(test_matrix))

    #check int_list
    print(int_list(5))
    print(int_list(8))
    print(int_list(1))

    #check permute_list
    a_list = ['a','b','c','d']
    perms = list(itertools.permutations(int_list(len(a_list))))
    print(perms)
    for perm in perms:
        print(permute_list(a_list, perm))
    print()

    #check symmetric permute
    a_matrix = [
        [ 1, 2, 3, 4],
        [ 5, 6, 7, 8],
        [ 9,10,11,12],
        [13,14,15,16]]
    print(perms[6])
    another_matrix = symmetric_permute(a_matrix, perms[6])
    print_m(another_matrix)

    #check get combs
    print(int_list(3))
    print(get_combs(int_list(3)))

    #check get_perms
    print(get_perms(int_list(3)))
    print()

    #check block permutations
    block = block_permutations(4)
    for b in block:
        print(b)
    print()

    a_matrix = a_matrix
    another_matrix = symmetric_permute(a_matrix, block[3])
    print(are_equal_adj(a_matrix, another_matrix)) # True
    another_matrix = symmetric_permute(a_matrix, perms[5])
    print(perms[5])             # Not a block permutation!
    print(are_equal_adj(a_matrix, another_matrix)) # False
    
