import copy
import Node
import fold_helper as fh
import make_legal as mleg

def next_edge_name(nodes):
    '''Given a list of nodes, this function returns a letter of the alphabet that has not
    already been used as a name. (In particular, the letter after the latest letter in the
    alphabet is returned.
    '''
    name_vals = []
    for node in nodes:
        name_vals.append(ord(node.name))
    new_name = chr(max(name_vals) + 1)
    return new_name

def make_new_edge(new_name, edge1, edge2, ht1, ht2):
    '''Given the nodes of the old graph, two edges to be folded partially, and the direction
    the fold is happening, this function creates the new node (or edge) resulting from that
    fold.
    '''
    name = new_name
    tail = [[edge1.name, ht1, True],[edge2.name, ht2, True]]
    if ht1 == "h":
        if ht2 == "h":
            head = fh.merge_ht(edge1.head, edge2.head)
        elif ht2 == "t":
            head = fh.merge_ht(edge1.head, edge2.tail)
    elif ht1 == "t":
        if ht2 == "h":
            head = fh.merge_ht(edge1.tail, edge2.head)
        elif ht2 == "t":
            head = fh.merge_ht(edge1.tail, edge2.tail)
    i = 0
    while i < len(head):
        if (head[i][0] == edge1.name and head[i][1] == ht1) or \
           (head[i][0] == edge2.name and head[i][1] == ht2):
            del head[i]
        else:
            i += 1
    return Node.Node(name, head, tail)

def fix_folded_edges(new_name, edge1, edge2, ht1, ht2):
    '''Given the name of a new edge resulting from a fold, the two edges to be folded
    partially and the direction the fold is happening, this function overwrites the folded
    direction on each edge to only the other edge and the new edge.
    '''
    if ht1 == "h":
        edge1.head = [[edge2.name, ht2, False],[new_name, "t", True]]
    elif ht1 == "t":
        edge1.tail = [[edge2.name, ht2, False],[new_name, "t", True]]
    if ht2 == "h":
        edge2.head = [[edge1.name, ht1, False],[new_name, "t", True]]
    elif ht2 == "t":
        edge2.tail = [[edge1.name, ht1, False],[new_name, "t", True]]

def fix_turns_ht(new_name, ht, edge1, edge2, ht1, ht2):
    '''From a head or tail attribute of a node of a graph, renames existing turns on it such
    that, as appropriate, they refer to the new edge (new_name) instead of the old ones
    (edge1 with ht1 and edge2 with ht2).
    '''
    first, second = None, None
    turn = 0
    while turn < len(ht):
        if ht[turn][0] == edge1.name and ht[turn][1] == ht1:
            ht[turn][0] = new_name
            ht[turn][1] = "h"
            first = turn
        elif ht[turn][0] == edge2.name and ht[turn][1] == ht2:
            ht[turn][0] = new_name
            ht[turn][1] = "h"
            second = turn
        turn += 1
    if first is not None and second is not None:
            ht[first][2] = ht[first][2] or ht[second][2]
            del ht[second]

def fix_turns(new_name, edges, edge1, edge2, ht1, ht2):
    '''Given the new name of an edge on a graph, the graph's edges, two edges to be folded
    partially, and the direction the fold is happening, this function renames existing turns
    to the edges such that, as appropriate, they refer to the new edge instead of the old
    ones.
    '''
    edge = 0
    while edge < len(edges):
        if edges[edge].name not in [edge1.name, edge2.name]: # We fix the not-folded edges
            fix_turns_ht(new_name, edges[edge].head, edge1, edge2, ht1, ht2)
            fix_turns_ht(new_name, edges[edge].tail, edge1, edge2, ht1, ht2)
        # Fix the not-folded directions on the folded edges
        elif edges[edge].name == edge1.name:
            if ht1 == "h":
                fix_turns_ht(new_name, edges[edge].tail, edge1, edge2, ht1, ht2)
            elif ht1 == "t":
                fix_turns_ht(new_name, edges[edge].head, edge1, edge2, ht1, ht2)
        elif edges[edge].name == edge2.name:
            if ht2 == "h":
                fix_turns_ht(new_name, edges[edge].tail, edge1, edge2, ht1, ht2)
            elif ht2 == "t":
                fix_turns_ht(new_name, edges[edge].head, edge1, edge2, ht1, ht2)
        edge += 1

def partial_fold(old_graph, edge1, ht1, edge2, ht2):
    '''Given a graph, two edges to be folded, and the directions the folding is happening,
    this function outputs a graph that is the original graph with the fold partially
    performed on it.
    '''
    graph = copy.deepcopy(old_graph)
    # alias the edges to those in the new graph
    edge1, edge2 = fh.find_edge(graph, edge1.name), fh.find_edge(graph, edge2.name)
    new_edge_name = next_edge_name(graph.nodes)
    fix_turns(new_edge_name, graph.nodes, edge1, edge2, ht1, ht2)
    graph.nodes.append(make_new_edge(new_edge_name, edge1, edge2, ht1, ht2))
    fix_folded_edges(new_edge_name, edge1, edge2, ht1, ht2)
    for edge in graph.nodes:
        fh.remove_self_connect(edge)
    mleg.remove_val_two_vertex(graph)
    graph.update_matrix()
    return graph
    

if __name__ == "__main__":
    import file_IO_helper as fio
##    # test next_edge_name
##    graph = fio.read_graph(0)
##    print(next_edge_name(graph.nodes)) # should be f
##    del graph.nodes[2]
##    print(next_edge_name(graph.nodes)) # should be f
##
##    # test folding
##    graph = fio.read_graph(0)
##    print("Graph we're starting with:")
##    graph.print_nodes()
##    folds = fh.fold_obj_to_name(graph.find_legal_folds())
##    fold = folds[0]
##    print("The fold we're doing:")
##    print(fold)
##    new = partial_fold(graph, fh.find_edge(graph, fold[0]), fold[1],
##                       fh.find_edge(graph, fold[2]), fold[3])
##    print("The graph we get:")
##    new.print_nodes()
##
##    # test again!
##    graph = fio.read_graph(1)
##    print("Graph we're starting with:")
##    graph.print_nodes()
##    folds = fh.fold_obj_to_name(graph.find_legal_folds())
##    fold = folds[0]
##    print("The fold we're doing:")
##    print(fold)
##    new = partial_fold(graph, fh.find_edge(graph, fold[0]), fold[1],
##                       fh.find_edge(graph, fold[2]), fold[3])
##    print("The graph we get:")
##    new.print_nodes()

##    i = 0
##    folder = "partial_fold_test"
##    while fio.graph_file(i, folder) != fio.next_graph(folder):
##        print(i)
##        graph = fio.read_graph(i, folder)
##        can_get_to = []
##        folds = fh.fold_obj_to_name(graph.find_legal_folds())
##        
##        for fold in folds:
##            new = partial_fold(graph, fh.find_edge(graph, fold[0]), fold[1],
##                               fh.find_edge(graph, fold[2]), fold[3])
##            ind = new.find_in_list(folder)
##            if ind is None:
##                file_name = fio.next_graph(folder)
##                fio.write_file(new, file_name)
##                can_get_to.append([fold, "p", fio.graph_index(file_name)])
##            else:
##                can_get_to.append([fold, "p", fio.graph_index(ind)])
##        graph.can_get_to = can_get_to
##        i += 1

##    folder = "partial_fold_test"
##    graph = fio.read_graph(1, folder)
##    fold = fh.fold_obj_to_name(graph.find_legal_folds())[0]
##    new = partial_fold(graph, fh.find_edge(graph, fold[0]), fold[1],
##                 fh.find_edge(graph, fold[2]), fold[3])
##    print(graph.is_equal(new))

    folder = "from_tri_reduced_partial"
    graph = fio.read_graph(6, folder)
    new = partial_fold(graph, fh.find_edge(graph, "b"), "t", fh.find_edge(graph, "d"), "h")
