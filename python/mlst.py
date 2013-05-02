import graph
import time

# Skeleton MLST class
class MLST:
    """
    NOTE: This is the base class. Any functionality that is generic across all subclasses
    must be implemented here to keep code DRY
    """
    def __init__(self):
        """
        Make the init take useful params for the algo, for potential tuning
        """
        pass

    def find_mlst(self, input_edge_set):
        """
        This is the main function that takes input edge_sets, and does magic
        to it to solve the problem
        """
        raise NotImplementedError


class BullshitMLST(MLST):
    """
    This is an example
    """
    def __init__(self, fuck=True, you=True):
        self.param_a = fuck
        self.param_b = you

    def find_mlst(self, input_edge_set):
        """
        fuck you
        """

        # install ipython, and you get to use this amazing tool
        # it goes into interactive shell mode, where you can tab-complete
        #import IPython; IPython.embed()

        return input_edge_set

class BruteforceMLST(MLST):
    """
    This is an example
    """
    def get_edge_permutation(self, edges):
        """
        returns all possible subsets of edges
        """
        import itertools
        for i in range(len(edges)):
            combos = itertools.combinations(edges, i+1)
            for s in combos: yield set(s)

    def find_mlst(self, input_edge_set):
        """
        This tries every subset of <input_edge_set>
        """
        #-------------------------------------------------------------
        best_leaves = 0
        best_edge_set = set()

        for edge_set in self.get_edge_permutation(input_edge_set):

            g = graph.make_graph(edge_set)
            g.search()

            if g.num_of_components == 1 and g.num_leaves > best_leaves:
                best_leaves = g.num_leaves
                best_edge_set = edge_set

        #-------------------------------------------------------------
        return best_edge_set

class SearchMLST(MLST):
    def generate_successors(self, input_edge_set):
        """
        Generate sucessor with only one node deleted
        """
        import itertools
        edge_list = list(input_edge_set)
        combos = itertools.combinations(input_edge_set, len(input_edge_set)-1)
        for s in combos: yield set(s)

    def find_mlst(self, input_edge_set):
        """
        BFS search to find an mlst
        """
        best_leaves = 0
        best_edge_set = set()
        closed = set()
        fringe = list()
        g = graph.make_graph(input_edge_set)
        g.search()
        num_nodes = g.num_nodes

        fringe.append(input_edge_set)

        while len(fringe) > 0: # list is not empty
            edge_set_node = fringe.pop()

            #== goal state ==#
            g = graph.make_graph(edge_set_node)
            g.search()

            if g.edges_in_one_component() and not g.has_cycle:
                if g.num_leaves > best_leaves:
                    best_leaves = g.num_leaves
                    best_edge_set =  edge_set_node

            #== expansion ==#

            edge_tuple = tuple( edge.__hash__()  for edge in edge_set_node )
            if edge_tuple not in closed:
                closed.add(edge_tuple)
                if len(edge_set_node) + 1 >= num_nodes: #if spanning tree is possible
                    for child in self.generate_successors(edge_set_node):
                        fringe.insert(0, child)
        return best_edge_set

class Timer:
    def __init__(self):
        self.start = time.time()
        self.elapsed = None
    def end(self):
        self.elapsed = time.time() -  self.start
        return self.elapsed
    def reset(self):
        self.start = time.time()
        self.elapsed = None

if __name__ == "__main__":

    import nbit
    CubitGenerator = nbit.CubitGenerator
    cubit_generator = CubitGenerator(3)
    # expand vertex 0 to "triplify" 48 times.
    # this would create a 100 node graph
    for i in range(3):
        cubit_generator.expand(vertex=0)

    timer = Timer()
    edge_set = cubit_generator.edges
    Brute = BruteforceMLST()

    mlst = Brute.find_mlst(edge_set)
    print "Found mlst %s!" % str(mlst)
    g = graph.make_graph(mlst)
    g.search()
    print "Found %d leaves!" % g.num_leaves

    print timer.end()

    timer.reset()
    Search = SearchMLST()
    mlst = Search.find_mlst(edge_set)
    print "Found mlst %s!" % str(mlst)
    g = graph.make_graph(mlst)
    g.search()
    print "Found %d leaves!" % g.num_leaves
    print timer.end()
