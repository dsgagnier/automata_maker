import fold_helper as fh

def sim_fold_names(graph):
    '''This function returns tuples that indicate folds done at the same vertex which may
    legally be done simultaneously.
    '''
    sim_folds = []
    legal = fh.fold_obj_to_name(graph.find_legal_folds())
    i = 0
    while i < len(legal):
        i_n = legal[i]
        j = i + 1
        while j < len(legal):
            j_n = legal[j]
            sim_legal = True
            combs = [fh.sort_to_str(i_n[0],i_n[1],j_n[0],j_n[1]),
                     fh.sort_to_str(i_n[0],i_n[1],j_n[2],j_n[3]),
                     fh.sort_to_str(i_n[2],i_n[3],j_n[0],j_n[1]),
                     fh.sort_to_str(i_n[2],i_n[3],j_n[2],j_n[3])]
            for comb in combs:
                if comb[:2] != comb[2:]:
                    if comb not in legal:
                        sim_legal = False
            if sim_legal == True:
                sim_folds.append([legal[i],legal[j]])
            j += 1
        i += 1
    return sim_folds

if __name__ == "__main__":
    import file_IO_helper as fio
    import strongly_connected_components as scc
    folder = "states_from_tri_and_ic"

##    graph = fio.read_graph(2)
##    node = graph.nodes[3]
##    node.head[0][2] = False
##    node = graph.nodes[1]
##    node.head[0][2] = False
##    print(sim_fold_names(graph)) # should not be empty!

    print("Let's try it on our automaton:")

    part = scc.partition_states(folder)
    #want to look at the second scc of 5 edge states
    print("five edges:")
    comps = scc.partition_part_scc(part[5], folder)[2]
    for state in comps:
        print(sim_fold_names(fio.read_graph(state, folder)))

    print("four edges:")
    comps = scc.partition_part_scc(part[4], folder)
    for comp in comps:
        for state in comp:
            print(state)
            print(sim_fold_names(fio.read_graph(state, folder)))

    print("three edges:")
    comps = scc.partition_part_scc(part[3], folder)
    for comp in comps:
        for state in comp:
            print(sim_fold_names(fio.read_graph(state, folder)))
