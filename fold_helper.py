def opp(ht):
    '''Switches "h" or "head" to "tail" and "t" or "tail" to head.
    '''
    if ht[0] == "h":
        return "tail"
    elif ht[0] == "t":
        return "head"

def merge_ht(ht1, ht2, keep_path = True):
    '''Given two head or tail lists (not necessarily both from the same
    type), this function merges them. It does not permit entries to contain both the same
    0th and 1st index as another entry. If there are two, and they disagree on the path
    indicator, it is set to True by default. If keep_path is false, then all path
    indicators added by ht2 are false
    '''
    new = [ x[:] for x in ht1]      # deep copy of ht1
    for ht in ht2:
        in_there = False
        i = 0
        # not len(new) because we don't have to check the stuff we just added to the list
        while i < len(ht1):
            if ht[0] == ht1[i][0] and ht[1] == ht1[i][1]:
                if ht[2] and keep_path:
                    new[i][2] = True # fix path indicator
                in_there = True
            i += 1
        if not in_there:
            new.append(ht[:] if keep_path else ht[:2] + [False])
    return new

def remove_self_connect(edge):
    '''This checks if the path is said to double back on an edge and removes it.
    '''
    i = 0
    while i < len(edge.head):
        if edge.head[i][0] == edge.name and edge.head[i][1] == "h":
            del edge.head[i]
        else:
            i += 1
    i = 0
    while i < len(edge.tail):
        if edge.tail[i][0] == edge.name and edge.tail[i][1] == "t":
            del edge.tail[i]
        else: i += 1
    return edge

def delete_folded_edges(all_edges, del_edges):
    '''Given a graph and a list of edges (that were presumably folded), this function
    deletes the folded nodes from the list of edges.
        We assume that none of the listed nodes are the last node in the list of edges.
    '''
    i = 0
    while i < len(all_edges) - 1:
        if all_edges[i].name in del_edges:
            del all_edges[i]
        else:
            i += 1

def find_edge(graph, edge_name):
    '''Given the graph and the name of an edge, returns the node in the graph
    representing that edge.
        We assume that there is only going to be one such node in the graph
    '''
    for node in graph.nodes:
        if node.name == edge_name:
            return node

def sort_to_str(one, ht_one, two, ht_two):
    '''Given two characters and their headtail indicators, returns a string of
    the characters concatenated with their indicators, with the order of the
    characters in the string being in alphabetical order.
    Example: ('a','h','b','t') -> 'ahbt'
             ('b','t','a','h') -> 'ahbt'
    '''
    if one < two:
        return one + ht_one + two + ht_two
    else:
        return two + ht_two + one + ht_one

def same_length_fold_allowed(node1, ht1, node2, ht2):
    '''Given two nodes to be folded along with the direction of the fold (eg head to head),
    this function returns True if a same length fold is allowed (would not change the rank
    of the graph) and False otherwise.
    '''
    if ht1 == "h":
        i = 0
        while i < len(node1.tail):
            if node1.tail[i][0] == node2.name and node1.tail[i][1] == opp(ht2)[0]:
                return False
            i += 1
    if ht1 == "t":
        i = 0
        while i < len(node1.head):
            if node1.head[i][0] == node2.name and node1.head[i][1] == opp(ht2)[0]:
                return False
            i += 1
    return True

def fold_obj_to_name(folds):
    '''Given a list of fold objects, returns a list of the distinct fold names in the list.
    '''
    names = []
    for fold in folds:
        if fold.fold_name not in names:
            names.append(fold.fold_name)
    return names
