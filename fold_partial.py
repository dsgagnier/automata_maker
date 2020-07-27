import copy
import Node
import fold_helper as fh

def next_edge_name(nodes):
    '''Given a list of nodes, this function returns a letter of the alphabet that has not
    already been used as a name. (In particular, the letter after the latest letter in the
    alphabet is returned.
    '''
    name_vals = []
    for node in nodes:
        name_vals.append(ord(node.name))
    return(chr(max(name_vals) + 1))
        

def partial_fold(old_graph, edge1, ht1, edge2, ht2):
    graph = copy.deepcopy(old_graph)
    
