import fold_same as fs
import fold_different as fd
import fold_helper as fh

class Fold:
    '''Describes a fold that can be performed on a graph.
    '''

    def __init__(self, graph_from, fold_name, longer, graph_to = "None"):
        '''Describes a fold that can be performed on a graph. Has as attributes the graph
        it goes from and (optionally) the graph it goes to, as well as its fold name (a
        string with formatting as "atet", and an indicator for the name of the edge which
        is longer (or is "same" if it's a same length fold).
        '''
        self.graph_from = graph_from
        self.graph_to = graph_to
        self.fold_name = fold_name
        self.longer = longer

    def perform_fold(self):
        '''Given a Fold, performs the fold on the graph specified in the object with the
        longer edge as specified. Returns the new graph.
        '''
        edge1 = fh.find_edge(self.graph_from, self.fold_name[0])
        edge2 = fh.find_edge(self.graph_from, self.fold_name[2])
        ht1, ht2 = self.fold_name[1], self.fold_name[3]
        if self.longer == "same":
            new = fs.same_length_fold(self.graph_from, edge1, ht1, edge2, ht2)
            return new
        elif self.longer == self.fold_name[0]:
            new = fd.diff_length_fold(self.graph_from, edge1, ht1, edge2, ht2)
            return new
        elif self.longer == self.fold_name[2]:
            new = fd.diff_length_fold(self.graph_from, edge2, ht2, edge1, ht1)
            return new
        
