import file_IO_helper as fio

def get_all_states_OLD(i = 0, folder = "states"):
    '''This gets all of the possible states of the automaton. We assume that
    in the folder, there is nothing but the initial states under file
    names graph_0, graph_1, ...

    This function assumes we are working in outer space without restrictions and that
    partial folds are not permitted
    '''
    while fio.graph_file(i, folder) != fio.next_graph(folder):
        print(i)
        graph = fio.read_graph(i, folder)
        print("These are the nodes of the graph we are folding:")
        graph.print_nodes()
        graph.perform_legal_folds(folder)
        fio.write_graph(graph, i, folder)
        i += 1
    print("WE DID IT")

def get_all_states(i = 0, folder = "states", partial = False, reduced_only = False):
    while fio.graph_file(i, folder) != fio.next_graph(folder):
        print(i)
        graph = fio.read_graph(i, folder)
        print("These are the nodes of the graph we are folding:")
        graph.print_nodes()
        graph.perform_legal_folds(folder, partial, reduced_only)
        fio.write_graph(graph, i, folder)
        i += 1
    print("WE DID IT!")

if __name__ == "__main__":
    get_all_states(folder = "from_tri_reduced_partial", partial = True, reduced_only = True)
    print('starting')
            
