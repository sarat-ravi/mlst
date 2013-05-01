import graph
from nbit import *

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
            for s in combos:
                yield set(s)

    def find_mlst(self, input_edge_set):
        """
        This tries every subset of <input_edge_set>
        """
        #-------------------------------------------------------------
        best_leaves = 0
        best_edge_set = set()

        i = 0
        print "finding mlst"
        for edge_set in self.get_edge_permutation(input_edge_set):
            print "iteration %d" % i

            g = graph.make_graph(edge_set)
            g.search()

            if g.num_of_components == 1 and g.num_leaves > best_leaves:
                best_leaves = g.num_leaves
                best_edge_set = edge_set

            i += 1

        #-------------------------------------------------------------
        return best_edge_set

if __name__ == "__main__":
    cubit_generator = CubitGenerator(3)
    # expand vertex 0 to "triplify" 48 times.
    # this would create a 100 node graph
    for i in range(48):
        cubit_generator.expand(vertex=0)

    # make sure stale data gets deleted
    cubit_generator.update_graph()

    # after
    edge_set = cubit_generator.edges

    Brute = BruteforceMLST()

    mlst = Brute.find_mlst(edge_set)

    print "Found mlst %s!" % str(mlst)
    g = graph.make_graph(mlst)
    g.search()
    print "Found %d leaves!" % g.num_leaves









