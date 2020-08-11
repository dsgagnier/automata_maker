import copy
import Node
import fold_helper as f
import make_legal as mleg

def make_new_edge(edge1, edge2, same_dir):
    '''Given two edges that are being folded (either head to head or head to tail) and
    considered to be the same length, this function returns the new node (or edge)
    resulting from that fold.
    '''
    name = edge1.name
    if same_dir:
        head = f.merge_ht(edge1.head, edge2.head)
        tail = f.merge_ht(edge1.tail, edge2.tail)
    else:
        head = f.merge_ht(edge1.head, edge2.tail)
        tail = f.merge_ht(edge1.tail, edge2.head)
    return Node.Node(name, head, tail)

def add_turns_by_turns(edgeht, turn, edge1, edge2, same_dir):
    '''Based on a turn in a graph, this function edits the turn to include additional
    turns gotten after a fold.
    
    Parameters:
    edgeht - the edge head or tail list that will need turns added to it
    turn - the turn that may require the addition of turns
    edge1, edge2, same_dir - the edges being folded with an indicator of whether they
            are being folded head to head
    '''
    if turn[0] == edge1.name:
        if turn[1] == "h":
            # if your edge is turning onto the head of edge1, then it's also turning
            # onto the head or tail of edge2, and needs the associated turns
            edgeht = f.merge_ht(edgeht, edge2.head, False) if same_dir else f.merge_ht(
                edgeht, edge2.tail, False)
        elif turn[1] == "t":
            edgeht = f.merge_ht(edgeht, edge2.tail, False) if same_dir else f.merge_ht(
                edgeht, edge2.head, False)
    if turn[0] == edge2.name:
        if turn[1] == "h":
            edgeht = f.merge_ht(edgeht, edge1.head, False) if same_dir else f.merge_ht(
                edgeht, edge1.tail, False)
        elif turn[1] == "t":
            edgeht = f.merge_ht(edgeht, edge1.tail, False) if same_dir else f.merge_ht(
                edgeht, edge1.head, False)
    return edgeht

def add_turns_to_edge(edge, edge1, edge2, same_dir):
    '''Based on the edge of a graph (parameter edge), this function edits its turns to
    include additional turns gotten after a fold.
    '''
    turn = 0
    while turn < len(edge.head):    # iterate through the turns the edge takes
        edge.head = add_turns_by_turns(edge.head, (edge.head)[turn], edge1, edge2, same_dir)
        turn += 1
    turn = 0
    while turn < len(edge.tail):
        edge.tail = add_turns_by_turns(edge.tail, (edge.tail)[turn], edge1, edge2, same_dir)
        turn += 1

def add_turns(graph, edge1, edge2, same_dir):
    '''Given a graph and the edges folded, this function gives to the other edges the turns
    that will be created from the fole.
    '''
    edge = 0
    while edge < len(graph.nodes):      #iterate through the edges in the graph
        add_turns_to_edge((graph.nodes)[edge], edge1, edge2, same_dir)
        edge += 1

def fix_turns_ht(ht, name1, name2, same_dir):
    '''Given the turns off the head or tail of an edge, the names of the edges that need to
    be identified, and an indicator of if they're being folded head-to-head, this function
    replaces all instances of name2 to name1, switching 'h' or 't' and the path indicator
    as appropriate
    '''
    j = 0
    first, second = [None, None], [None, None]
    while j < len(ht):
        if ht[j][0] == name1:
            if ht[j][1] == "h":
                first[0] = j
            elif ht[j][1] == "t":
                first[1] = j
        elif ht[j][0] == name2:
            ht[j][0] = name1
            if not same_dir:
                ht[j][1] = f.opp(ht[j][1])[0]
            # if the direction we're turning onto will be identified with edge1.head
            if ht[j][1] == "h" :
                second[0] = j
            elif ht[j][1] == "t":
                second[1] = j
        j += 1
    to_delete = []
    for j in [0,1]:
        if first[j] is not None and second[j] is not None:
            ht[first[j]][2] = ht[first[j]][2] or ht[second[j]][2]
            to_delete.append(second[j])     # delete the copies
    to_delete.sort(reverse = True)
    for ind in to_delete:   # delete in decending order to not shift indices
        del ht[ind]

def fix_turns(graph, edge1, edge2, same_dir):
    '''Given a graph, this function renames existing turns on the edges so that, instead of
    referring to the folded edges, they refer to the new edge gotten from the fold.
    '''
    i = 0
    while i < len(graph.nodes):
        fix_turns_ht((graph.nodes[i]).head, edge1.name, edge2.name, same_dir)
        fix_turns_ht((graph.nodes[i]).tail, edge1.name, edge2.name, same_dir)
        i += 1

def same_length_fold(old_graph, edge1, ht1, edge2, ht2):
    '''Given a graph, two edges to be folded, and the directions the folding is happening,
    this function outputs a graph that is the original graph with the fold performed in it
    as if both edges are the same length.
    '''
    graph = copy.deepcopy(old_graph)
    graph.nodes.append(make_new_edge(edge1, edge2, ht1 == ht2))
    add_turns(graph, edge1, edge2, ht1 == ht2)
    fix_turns(graph, edge1, edge2, ht1 == ht2)
    f.delete_folded_edges(graph.nodes, [edge1.name, edge2.name])
    for edge in graph.nodes:
        f.remove_self_connect(edge)
    mleg.remove_val_two_vertex(graph)
    graph.update_matrix()
    return graph

if __name__ == "__main__":
    import file_IO_helper as fio
    import adj_matrices as adj
    # Testing is out of date, but functions should still work
##    graphs = fio.read_file("graphs")
##    fold_from = graphs[0]
##    old_graph = copy.deepcopy(graphs[0])    # node order goes a, b, d, e, c
##
##    # check same length folds
##    new_graph = same_length_fold(fold_from, fold_from.nodes[0], "t", fold_from.nodes[3], "t")
##    print(fold_from.is_equal(old_graph))    # check that we don't change the original grpah
##    for node in new_graph.nodes:
##        print(node.name)
##    adj.print_m(new_graph.matrix)

    graph = fio.read_graph(28) # nodes are in the order b,d,c,a
    new = same_length_fold(graph, graph.nodes[3], 't', graph.nodes[0], 'h') # folding atbh;s
    print("This is the resulting graph")
    new.print_nodes()
    
