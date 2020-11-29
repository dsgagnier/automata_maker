import itertools
import adj_matrices as adj
import fold_helper as fh
import Fold as f
import file_IO_helper as fio
import copy

class Graph:
    '''A graph contains a collection of node objects.'''
    
    def __init__(self, nodes, shape = "", num = ""):
        self.nodes = nodes
        self.shape = shape
        self.num = num
        self.matrix = adj.nodes_to_matrix(nodes)
        self.can_get_to = []

    def update_matrix(self):
        self.matrix = adj.nodes_to_matrix(self.nodes)

    def is_equal(self, other_graph):
        '''Given two graphs, returns True is the matrices of the graphs are equal up to
        symmetric permutation. Returns False otherwise.
        '''
        return adj.are_equal_adj(self.matrix, other_graph.matrix)

    def print_nodes(self):
        '''Prints the nodes of a graph.'''
        for node in self.nodes:
            print("Name: " + node.name)
            print("Head: ")
            print(node.head)
            print("Tail: ")
            print(node.tail)
            print()

    def in_list(self, folder = "states"):
        '''This function checks if the "self" object is equal to any graph in the states
        folder via linear search.
        '''
        i = 0
        graphs_left = True
        while graphs_left:
            try:
                if self.is_equal(fio.read_graph(i, folder = "states")):
                    return True
                i += 1
            except:
                graphs_left = False
        return None

    def find_in_list(self, folder = "states"):
        '''This function checks if the "self" object is equal to any graph in the specified
        folder via linear search. If so, it returns the file name. Otherwise, it returns
        None.
        '''
        i = 0
        graphs_left = True
        while graphs_left:
            try:
                if self.is_equal(fio.read_graph(i, folder)):
                    return fio.graph_file(i, folder)
                i += 1
            except:
                graphs_left = False
        return None

    def get_vertices(self):
        '''Given a graph, this function returns a list where each element is a list
        representing the directions that can be taken at a given vertex. Effectively,
        this function returns a list of vertices.
        '''
        verts = []
        for edge in self.nodes:
            in_already_h, in_already_t = False, False
            for vert in verts:
                if edge.name + "h" in vert:
                    in_already_h = True
            if not in_already_h:
                new = [edge.name + "h"]
                for turn in edge.head:
                    new.append(turn[0] + turn[1])
                verts.append(new)
            for vert in verts:
                if edge.name + "t" in vert:
                    in_already_t = True
            if not in_already_t:
                new = [edge.name + "t"]
                for turn in edge.tail:
                    new.append(turn[0] + turn[1])
                verts.append(new)
        return verts

    def adjacent_vertices(self, vertices, vertex):
        '''Given a list of vertices in a graph (as calculated by get_vertices() and the
        index of a specific vertex in that list, this function returns the indices of all
        adjacent vertices.
        '''
        adj = []
        vertex = vertices[vertex]
        for outneigh in vertex: # see which vertex each outgoing edge goes to
            other_end = outneigh[0] + fh.opp(outneigh[1])[0]
            i = 0
            while i < len(vertices):
                if other_end in vertices[i] and i not in adj:
                    adj.append(i)
                i += 1
        return sorted(adj)
    
    def find_legal_folds(self, partial = False, same = True):
        '''Given a graph, this function determines what the legal folds on this graph are.
        It returns the folds as a list of Fold objects.
        '''
        names = []
        folds = []
        for edge in self.nodes:
            for turn in edge.head:
                fold_on = fh.find_edge(self, turn[0])
                fold_name = fh.sort_to_str(edge.name, "h", turn[0], turn[1])
                if fold_name[0] == fold_name[2]:    # This is only a legal partial fold
                    if partial:
                        folds.append(f.Fold(self, fold_name, "partial"))
                    else:
                        pass
                elif fold_name not in names and turn[2] == False:
                    names.append(fold_name)
                    if same and fh.same_length_fold_allowed(edge, "h", fold_on, turn[1]):
                        folds.append(f.Fold(self, fold_name, 'same'))
                    folds.append(f.Fold(self, fold_name, edge.name))
                    folds.append(f.Fold(self, fold_name, turn[0]))
                    if partial:
                        folds.append(f.Fold(self, fold_name, "partial"))
            # Same thing, but in tail
            for turn in edge.tail:
                fold_on = fh.find_edge(self, turn[0])
                fold_name = fh.sort_to_str(edge.name, "t", turn[0], turn[1])
                if fold_name[0] == fold_name[2]:
                    # legal as a partial fold, but that would be accounted for in the
                    # head section
                    pass
                elif fold_name not in names and turn[2] == False:
                    names.append(fold_name)
                    if same and fh.same_length_fold_allowed(edge, "t", fold_on, turn[1]):
                        folds.append(f.Fold(self, fold_name, 'same'))
                    folds.append(f.Fold(self, fold_name, edge.name))
                    folds.append(f.Fold(self, fold_name, turn[0]))
                    if partial:
                        folds.append(f.Fold(self, fold_name, "partial"))
        return folds

    def vertices_with_folds(self):
        '''This function returns a list of vertices (as from the get_vertices function)
        where legal folds may be performed.
        '''
        verts = self.get_vertices()
        folds = self.find_legal_folds()
        indices_w_folds = []
        vertices_w_folds = []
        for fold in folds:
            i = 0
            while i < len(verts):
                if fold.fold_name[:2] in verts[i]:
                    if i not in indices_w_folds:
                        indices_w_folds.append(i)
                i += 1
        for ind in indices_w_folds:
            vertices_w_folds.append(verts[ind])
        return vertices_w_folds

    def perform_legal_folds(self, folder = "states", partial = False, reduced_only = False, same = True):
        '''Performs all legal folds on a graph stored in the specifed folder.
        '''
        can_get_to = []
        folds = self.find_legal_folds(partial, same)
        print()
        print("new graph")
        for fold in folds:
            print(fold.fold_name)
            print(fold.longer)

        for fold in folds:
            new = fold.perform_fold()
            print("We performed the fold:")
            print(fold.fold_name)
            print(fold.longer)
            if not reduced_only or new.is_reduced():
                print("It gave the graph:")
                new.print_nodes()
                ind = new.find_in_list(folder)
                print("Is it in the list? If so, what's its file name?")
                print(ind)
                if ind is None:     # we haven't already seen the graph gotten from fold
                    file_name = fio.next_graph(folder)
                    fio.write_file(new, file_name)
                    can_get_to.append([fold.fold_name, fold.longer, fio.graph_index(file_name)])
                else:
                    can_get_to.append([fold.fold_name, fold.longer, fio.graph_index(ind)])
                print("did a fold")
        self.can_get_to = can_get_to

    def is_connected(self, starting = None, seen = None):
        '''A recursive function that checks if a graph is connected. Code adapted from:
        https://www.python-course.eu/graphs_python.php
        '''
        if starting is None:
            starting = self.nodes[0]
        if seen is None:
            seen = []
        seen.append(starting.name)
        if len(seen) != len(self.nodes): # We haven't seen every edge
            for turn in starting.head:
                if turn[0] not in seen:
                    if self.is_connected(fh.find_edge(self, turn[0]), seen):
                        return True
            for turn in starting.tail:
                if turn[0] not in seen:
                    if self.is_connected(fh.find_edge(self, turn[0]), seen):
                        return True
        else:
            return True
        return False

    def delete_node(self, node):
        '''Deletes the specified node from the graph.'''
        self.nodes.remove(node)
        for edge in self.nodes:
            turn = 0
            while turn < len(edge.head):
                if edge.head[turn][0] == node.name:
                    del edge.head[turn]
                else:
                    turn += 1
            turn = 0
            while turn < len(edge.tail):
                if edge.tail[turn][0] == node.name:
                    del edge.tail[turn]
                else:
                    turn += 1
                    
    def is_reduced(self):
        '''Determines if the graph is reduced (ie does not have a separating edge)'''
        i = 0
        while i < len(self.nodes):
            graph = copy.deepcopy(self)
            graph.delete_node(graph.nodes[i])
            if not graph.is_connected():
                return False
            i += 1
        return True

if __name__ == "__main__":
    import file_IO_helper as fio
    import adj_matrices as adj
    import Fold as f
##    graph_0 = fio.read_graph(0)
##    graph_0.perform_legal_folds()
##    graph_1 = fio.read_graph(1)
##    graph_1.perform_legal_folds()

##    graph_1 = fio.read_graph(1)
##    folds = graph_1.find_legal_folds()
##    print("The legal folds are:")
##    for fold in folds:
##        print(fold.fold_name)

##    graph = fio.read_graph(0)
##    verts = graph.get_vertices()
##    for vert in verts:
##        print(vert)
##    print(graph.vertices_with_folds())
##
##    # Let's see if there are any graphs with more than one vertex with a legal fold
##    i = 0
##    while i < 211:
##        g = fio.read_graph(i)
##        v = g.vertices_with_folds()
##        if len(v) > 1:
##            print(i)
##            print(len(v))
##            print(len(g.nodes))
##            print()
##        i += 1
##
##    # Let's see if there are any 5-edge graphs w more than one vertex w a legal fold
##    i = 0
##    while i < 211:
##        g = fio.read_graph(i)
##        v = g.vertices_with_folds()
##        if len(v) > 1 and len(g.nodes) == 5:
##            print(i)
##            print(len(v))
##        i += 1

##    # test get_vertices() and adjacent_vertices()
##    graph = fio.read_graph(0)
##    verts = graph.get_vertices()
##    print(verts)
##    for i in range(len(verts)):
##        print(graph.adjacent_vertices(verts, i))
##    #test is_reduced
##    print(graph.is_reduced())
##
##    # test vertices again
##    graph = fio.read_graph(1, "states_from_tri_and_ic")
##    verts = graph.get_vertices()
##    print(verts)
##    for i in range(len(verts)):
##        print(graph.adjacent_vertices(verts, i))
##
##    # test is connected
##    folder = "states_from_tri_and_ic"
##    i = 0
##    while i < 50:
##        graph = fio.read_graph(i, folder)
##        print(i)
##        print(graph.is_reduced())
##        i += 1
##    print(fio.read_graph(102, folder).is_reduced())
    print()
