import pickle

def read_file(file_name):
    '''Reads a pickled file with file_name. Returns the object that was pickled.'''
    infile = open(file_name,"rb")
    obj = pickle.load(infile)
    infile.close()
    return obj

def write_file(obj, file_name):
    '''Pickles an object under file_name.'''
    outfile = open(file_name,"wb")
    pickle.dump(obj,outfile)
    outfile.close()

def graph_file(integer, folder = "states"):
    '''Returns a file name in format of the folder name concatenated with the "/graph_" and
    the integer. By default: "states/graph_integer".
    '''
    file_name = folder + "/graph_" + str(integer)
    return file_name

def read_graph(integer, folder = "states"):
    '''Reads the file of the graph associated with the specified integer in a provided
    folder (by default, "states").
    '''
    return read_file(graph_file(integer, folder))

def write_graph(obj, integer, folder = "states"):
    '''Pickles an object under the file name for a graph with the specified integer in a
    folder that's specified or by default "states".
    '''
    return write_file(obj, graph_file(integer, folder))

def next_graph(folder = "states"):
    '''Returns the file name of the next graph to be added to a specified folder, or by
    default, the folder "states".
    '''
    i = 0
    while True:
        try:
            read_graph(i, folder)
            i += 1
        except:
            return graph_file(i, folder)

def graph_index(file_name):
    '''Given the file name of a graph, returns the integer tacked onto the end.'''
    integer = file_name[file_name.rfind("_") + 1 :]  # take from the _ to the end
    return int(integer)

if __name__ == "__main__":
    print("hi")
##    test = read_file(graph_file(0))
##    print(next_graph())
##    print(graph_index("/states/graph_101"))
##    print(graph_index("/states/graph_5"))

    # test update to folder name functionality
    i = 0
    while i < graph_index(next_graph("states_from_tri_graph")):
        print(graph_file(i, "states_from_tri_graph"))
        i += 1
