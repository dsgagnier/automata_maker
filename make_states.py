import file_IO_helper as fio

def get_all_states():
    '''This gets all of the possible states of the automaton. We assume that
    in the states folder, there is nothing but the initial state under file
    name graph_0.
    '''
    i = 0
    while fio.graph_file(i) != fio.next_graph():
        print(i)
        graph = fio.read_graph(i)
        print("These are the nodes of the graph we are folding:")
        graph.print_nodes()
        graph.perform_legal_folds()
        fio.write_graph(graph, i)
        i += 1
    print("WE DID IT")

if __name__ == "__main__":
    #get_all_states()
    print('starting')
