import file_IO_helper as fio

def get_all_states(i = 0, folder = "states"):
    '''This gets all of the possible states of the automaton. We assume that
    in the states folder, there is nothing but the initial state under file
    name graph_0.
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

if __name__ == "__main__":
    get_all_states(i = 211, folder = "states_from_tri_and_ic")
    print('starting')
