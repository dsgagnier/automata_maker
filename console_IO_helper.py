import Node
import Graph

def input_checker(message, permissible = ["yes","y","no","n"]):
    '''Given a prompt to the user and a list of permissible inputs, this function
    ensures that the user gives a permissible input to the prompt, getting the user to
    reenter the input if it is invalid.
        The function returns the input in lower case and assumes the list of permissible
    inputs are all in lower case. If no permissible list is given, a yes/no question
    is assumed
    '''
    rep = True
    while rep:
        userin = input(message + " ").lower()
        if userin in permissible:
            rep = False
        else:
            print("Invalid input. Try again.")
    return userin.lower()

def enter_headtail():
    '''Prompts the user to enter in the information for a "head" or "tail" entry
    in a node object. That is, the user indicates what other edges (and which end of them)
    a given end of an edge in the graph is connected to. Information about whether the
    path on the graph goes over the specified turn is also provided by the user.
    '''

    dest = input("Enter the destination.")
    headtail = input_checker("Does it go to the head or the tail?",
                             ["h","t","head","tail"])[0]
    path = input_checker("Does the path go over this turn?",
                         ["y","n","yes","no"])[0]
    path = True if path == "y" else False
    return [dest,headtail,path]

def enter_headtail_mult():
    '''Prompts the user to enter any number of head or tail entries for a node object.
    '''
    userin = "y"
    mults = []

    while userin == "y":
        mults.append(enter_headtail())
        userin = input_checker("Would you like to enter another? Enter yes/no:",
                               ["yes","y","no","n"])[0]
    return mults

def enter_node():
    '''This prompts the user to enter in information that is then used to create a
    node object.
    '''
    name = input("Enter edge name.")[0]
    print("Please enter where we can go from the head of the edge.")
    h = enter_headtail_mult()
    print()
    print("Please enter where we can go from the tail of the edge.")
    t = enter_headtail_mult()
    print()
    return Node.Node(name,h,t)

def enter_node_mult():
    '''Prompts the user to enter information for any number of node objects.
    '''
    userin = "y"
    mults = []

    while userin == "y":
        mults.append(enter_node())
        userin = input_checker("Would you like to enter another edge? Enter yes/no:",
                               ["yes","y","no","n"])[0]
    return mults

def enter_graph():
    '''Prompts the user to enter information for a graph object.
    '''
    shape = input("Enter the type of graph or leave an empty line:")
    print()
    num = input("Enter the number of the type of graph (eg for TRI.II enter 2)" +
                " or leave an empty line:")
    print()
    print("Now please enter the edges of the graph.")
    nodes = enter_node_mult()
    return Graph.Graph(nodes,shape,num)

def print_graphs(graphs):
    '''Prints a list of graphs.'''
    i = 0
    while i < len(graphs):
        print("Graph " + str(i) + ": " + graphs[i].to_string())
        i += 1
