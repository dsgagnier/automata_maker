import copy
import Node
import fold_helper as f

def make_new_edge(edge_long, ht_long, edge_short, ht_short):
    '''Given two edges that are being folded (with the direction of folidng along the edges
    given), with edge_long considered longer), this function returns the new node (or edge)
    resulting from that fold (which is essentially the leftover part of edge_long that did
    not get folded).
    '''
    name = edge_long.name
    if ht_long == "h":
        if ht_short == "h":
            head = [x[:2] + [False] for x in edge_short.tail] #Ensure correct path indicator
        elif ht_short == "t":
            head = [x[:2] + [False] for x in edge_short.head]
        head.append([edge_short.name, f.opp(ht_short)[0], True])
        tail = [x[:] for x in edge_long.tail]
    elif ht_long == "t":
        if ht_short == "h":
            tail = [x[:2] + [False] for x in edge_short.tail]
        elif ht_short == "t":
            tail = [x[:2] + [False] for x in edge_short.head]
        tail.append([edge_short.name, f.opp(ht_short)[0], True])
        head = [x[:] for x in edge_long.head]
    return Node.Node(name, head, tail)

def fix_short_edge(edge_long, ht_long, edge_short, ht_short):
    '''Given two edges that are being folded (with direction of folding indicated), this
    function fixes the short edge so that all of the turns on it are correct.
    '''
    if ht_short == "h":
        if ht_short == ht_long:
            # Even though they already have the same turns, we merge the nodes to make
            # sure the path indicator is correct
            edge_short.head = f.merge_ht(edge_short.head, edge_long.head)
        else:
            edge_short.head = f.merge_ht(edge_short.head, edge_long.tail)
        edge_short.tail.append([edge_long.name, ht_long, True])
    elif ht_short == "t":
        if ht_short == ht_long:
            edge_short.tail = f.merge_ht(edge_short.tail, edge_long.tail)
        else:
            edge_short.tail = f.merge_ht(edge_short.tail, edge_long.head)
        edge_short.head.append([edge_long.name, ht_long, True])
    #return (edge_short.head, edge_short.tail)

def add_turns_to_ht(ht, edge_long, ht_long, edge_short, ht_short):
    '''Given a list of turns from a head or tail list of a node and a fold of edges of
    different lengths, this function adds a new turn created by the fold to the head or
    tail list if appropriate.
    '''
    i = 0
    while i < len(ht):
        turn = ht[i]
        # If we are at the vertex where the new edge is coming out of
        if turn[0] == edge_short.name and turn[1] == f.opp(ht_short)[0]:
            ht.append([edge_long.name, ht_long, False])
        i += 1

def add_turns(edges, edge_long, ht_long, edge_short, ht_short):
    '''Given a fold of edges of different lengths, this function gives the other edges
    of a graph turns that will be created from the fold. Namely, turns will only be
    introduced at the vertex where edge_long and the new edge meet, and the new turns will
    only be going from a previously existing edge to the new edge.
    '''
    edge = 0
    while edge < len(edges):
        add_turns_to_ht(edges[edge].head, edge_long, ht_long, edge_short, ht_short)
        add_turns_to_ht(edges[edge].tail, edge_long, ht_long, edge_short, ht_short)
        edge += 1

def fix_turns_of_ht(ht, edge_long, ht_long, edge_short, ht_short):
    '''Given a list of turns from a head or tail list of a node and a fold of edges of
    different lengths, this function renames existing turns on the edges so that they
    refer to the new edge instead of folded edges where appropriate. Note that turns are
    only going to have to be fixed at the vertex where the fold occured.
    '''
    turn = 0
    short, long = None, None
    while turn < len(ht):
        if ht[turn][0] == edge_long.name and ht[turn][1] == ht_long:
            ht[turn][0] = edge_short.name
            ht[turn][1] = ht_short
            long = turn
        elif ht[turn][0] == edge_short.name and ht[turn][1] == ht_short:
            short = turn
        turn += 1
    if short is not None and long is not None:
        ht[short][2] = ht[short][2] or ht[long][2] # ensure correctness of path indicator
        del ht[long]
            
    

def fix_turns(edges, edge_long, ht_long, edge_short, ht_short):
    '''Given a graph and a fold of edges with different lengths, this function renames
    existing turns on the edges so that, instead of referring to the folded edges, they
    refer to the new edge gotten from the fold when appropriate.
    '''
    edge = 0
    while edge < len(edges):
        fix_turns_of_ht(edges[edge].head, edge_long, ht_long, edge_short, ht_short)
        fix_turns_of_ht(edges[edge].tail, edge_long, ht_long, edge_short, ht_short)
        edge += 1
    

def diff_length_fold(old_graph, edge_long, ht_long, edge_short, ht_short):
    '''Given a graph, two edges to be folded, and the directions the folding is happening,
    this function outputs a graph that is the original graph with the fold performed in it
    as if edge_long is longer than edge_short.
    '''
    graph = copy.deepcopy(old_graph)
    edge_long = f.find_edge(graph, edge_long.name)    # Set the variables to the nodes in
    edge_short = f.find_edge(graph, edge_short.name)  # the new graph
    
    fix_turns(graph.nodes, edge_long, ht_long, edge_short, ht_short)
    graph.nodes.append(make_new_edge(edge_long, ht_long, edge_short, ht_short))
    fix_short_edge(edge_long, ht_long, edge_short, ht_short)
    add_turns(graph.nodes, edge_long, ht_long, edge_short, ht_short)
    f.delete_folded_edges(graph.nodes, [edge_long.name])
    for edge in graph.nodes:
        f.remove_self_connect(edge)
    graph.update_matrix()
    return graph

if __name__ == "__main__":
    # Testing is out of date, but functions should still work
    print()
##    import file_IO_helper as fio
##    import adj_matrices as adj
##    graphs = fio.read_file("graphs")
##    fold_from = graphs[0]
##    old_graph = copy.deepcopy(graphs[0])    # node order goes a, b, d, e, c
##
##    # check same length folds
##    new_graph = diff_length_fold(fold_from, fold_from.nodes[0], "t", fold_from.nodes[3], "t")
##    print(fold_from.is_equal(old_graph))    # check that we don't change the original graph
##    adj.print_m(new_graph.matrix)
