import Node
import fold_helper as fh
import copy

def find_val_two_vertex(graph):
    '''Finds and returns a valence two vertex in the graph if it exists. Returns None
    otherwise. This function only returns one vertex of valence two, even if more than one
    exists. (Only one should ever arise as a result of a partial fold.
    '''
    vertices = graph.get_vertices()
    for vert in vertices:
        if len(vert) == 2:
            return vert

def make_merged_edge(edge1, ht1, edge2, ht2):
    '''Given two edges in a graph that should be merged along with the turn at which they
    should be merged, this function returns the merged edge.
    '''
    name = edge1.name
    if ht1 == "h":
        tail = copy.deepcopy(edge1.tail)
        head = copy.deepcopy(edge2.tail) if ht2 == "h" else copy.deepcopy(edge2.head)
    elif ht1 == "t":
        head = copy.deepcopy(edge1.head)
        tail = copy.deepcopy(edge2.tail) if ht2 == "h" else copy.deepcopy(edge2.head)
    return Node.Node(name, head, tail)

def fix_turns_merge_ht(ht, edge1, ht1, edge2, ht2):
    '''This function fixes references in a head or tail list of a node to the edges that
    were merged, to ensure that they refer to the appropriate edges.
    '''
    turn = 0
    while turn < len(ht):
        if ht[turn][0] == edge2.name and ht[turn][1] == fh.opp(ht2)[0]:
            ht[turn][0] = edge1.name
            ht[turn][1] = ht1
        turn += 1

def fix_turns_merge(graph, edge1, ht1, edge2, ht2):
    '''This function fixes references in graph.nodes to the edges that were merged, to
    ensure that they refer to the appropriate edges.
    '''
    edge = 0
    while edge < len(graph.nodes):
        fix_turns_merge_ht(graph.nodes[edge].head, edge1, ht1, edge2, ht2)
        fix_turns_merge_ht(graph.nodes[edge].tail, edge1, ht1, edge2, ht2)
        edge += 1

def remove_val_two_vertex(graph):
    '''Given a graph, this function removes a valence-two vertex if one exists.
    '''
    vertex = find_val_two_vertex(graph)
    if vertex is not None:
        edge1 = fh.find_edge(graph, vertex[0][0])
        edge2 = fh.find_edge(graph, vertex[1][0])
        ht1, ht2 = vertex[0][1], vertex[1][1]
        graph.nodes.append(make_merged_edge(edge1, ht1, edge2, ht2))
        fix_turns_merge(graph, edge1, ht1, edge2, ht2)
        fh.delete_folded_edges(graph.nodes, [edge1.name, edge2.name])
        graph.update_matrix
    else:
        return
