import fold_helper as fh

def sim_fold_names(graph):
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

    graph = fio.read_graph(2)
    node = graph.nodes[3]
    node.head[0][2] = False
    node = graph.nodes[1]
    node.head[0][2] = False
    print(sim_fold_names(graph)) # should not be empty!

    print("Let's try it on our automaton:")

    part = scc.partition_states()
    #want to look at the second scc of 5 edge states
    print("five edges:")
    comps = scc.partition_part_scc(part[5])[1]
    for state in comps:
        print(sim_fold_names(fio.read_graph(state)))

    print("four edges:")
    comps = scc.partition_part_scc(part[4])
    for comp in comps:
        for state in comp:
            print(state)
            print(sim_fold_names(fio.read_graph(state)))

    print("three edges:")
    comps = scc.partition_part_scc(part[3])
    for comp in comps:
        for state in comp:
            print(sim_fold_names(fio.read_graph(state)))
