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

def graph_file(integer):
    '''Returns a file name in format "states/graph_integer".'''
    file_name = "states/graph_" + str(integer)
    return file_name

def read_graph(integer):
    '''Reads the file of the graph associated with the specified integer.'''
    return read_file(graph_file(integer))

def write_graph(obj, integer):
    '''Pickles an object under the file name for a graph with the specified integer.'''
    return write_file(obj, graph_file(integer))

def next_graph():
    '''Returns the file name of the next graph to be added to the folder.'''
    i = 0
    while True:
        try:
            read_graph(i)
            i += 1
        except:
            return graph_file(i)

def graph_index(file_name):
    '''Given the file name of a graph, returns the integer tacked onto the end.'''
    integer = file_name[file_name.find("_") + 1 :]  # take from the _ to the end
    return int(integer)

if __name__ == "__main__":
    print("hi")
    test = read_file(graph_file(0))
    print(next_graph())
    print(graph_index("/states/graph_101"))
    print(graph_index("/states/graph_5"))
