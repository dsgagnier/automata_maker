import file_IO_helper as fio

def get_all_states(i = 0, folder = "states", partial = False, reduced_only = False, same = True):
    while fio.graph_file(i, folder) != fio.next_graph(folder):
        print(i)
        graph = fio.read_graph(i, folder)
        print("These are the nodes of the graph we are folding:")
        graph.print_nodes()
        graph.perform_legal_folds(folder, partial, reduced_only, same)
        fio.write_graph(graph, i, folder)
        i += 1
    print("WE DID IT!")

if __name__ == "__main__":
    get_all_states(folder = "rank_4", partial = False, reduced_only = False, same = False)
    print('starting')
            
