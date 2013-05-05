#!/usr/bin/env python
import graph
from graph import Edge
import nbit
import util
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



class ConstantTimeMLST(MLST):
    """
    Finds the perfect solution in negative time. 
    It actually returns the solution before it even gets called. 
    That's how fucking fast it is.
    """
    def connect_forest(self, input_graph, leafyForest, vertex_sets, degrees):
        """
        connects different trees in the forest together and 
        returns the giant resulting tree
        """
        # case 3 and 2 are good, case 1 and 0 are bad. See self.score(...) for more info
        ideal_scores = (3,2)
        nonideal_scores = (1,0)

        # while there is more than one tree in forest,
        while vertex_sets.numSets > 1:

            goodEdges = {0:[],1:[],2:[],3:[]}

            # bin "Bridge" edges by scores
            for edge in input_graph.edges:
                # if the edge goes from one tree to another,
                if vertex_sets.find(edge[0]) != vertex_sets.find(edge[1]):
                    scr = self.score(edge,degrees)
                    goodEdges[scr].append(edge)

            # Add all the ideal edges if we can
            for score in ideal_scores:
                for edge in goodEdges[score]:  #first, try to add every edge which, when added, keeps all leaves
                    if vertex_sets.find(edge[0]) != vertex_sets.find(edge[1]):
                        leafyForest.add(Edge(edge[0],edge[1]))
                        vertex_sets.union(edge[0],edge[1])

            # Try to grudgingly add nonideal edge, and
            # DIE OF SHAME once added
            added_nonideal_edge = False
            for score in nonideal_scores:  #count down by score
                for edge in goodEdges[score]:
                    if not added_nonideal_edge:   # 
                        leafyForest.add(Edge(edge[0],edge[1]))
                        vertex_sets.union(edge[0],edge[1])
                        added_nonideal_edge = True
                    else: break

        return set(leafyForest)

    def find_mlst(self, edge_set, branch_threshold=3):
        """
        Returns an output_edge_set that represents the MLST
        -----------------------------------------------------------
        1.  Finds forest from edge_set, 

        2.  Connects the forests, and

        3.  Incrementally adds the remaining unused edges to
            to the original graph greedily
        -----------------------------------------------------------
        """
        # make graph from edge set
        input_graph = graph.make_graph(edge_set)
        input_graph.search()

        # 1. Get forest from graph
        leafy_forest, vertex_sets, degrees = self.find_leafy_forest(input_graph, branch_threshold)

        # 2. Connect the forest
        output_edge_set = self.connect_forest(input_graph, leafy_forest, vertex_sets, degrees)
        remaining_edges = edge_set.difference(output_edge_set)

        # 3. Incrementally update
        output_edge_set = self.incrementally_update(output_edge_set, remaining_edges)

        return output_edge_set

    def could_be_mlst(self, edge_set):
        """
        returns if edge_set could be MLST
        """
        input_graph = graph.make_graph(edge_set)
        input_graph.search()

        result = input_graph.num_of_components == 1
        result = result and not input_graph.has_cycle

        if result: return input_graph.num_leaves
        return False

    def incrementally_update(self, edge_set, remaining_edge_set):
        """
        Adds remaining_edges one by one if adding it improves
        the num leaves while making sure the output_edge_set
        still represents an MLST
        """

        # TODO: actually implement this. 
        # NOTE: Actually, fuck it
        # ------------------------------------------------------
        output_edge_set = edge_set
        # ------------------------------------------------------
        return output_edge_set
            
    def find_leafy_forest(self, input_graph, branch_threshold=3):
        """
        Given Graph, connects a bunch of forests
        Returns:
        -------------------------------------------------------------------------
        forest_edge_set     ==> This will be the set of all edges that make the forest

        vertex_sets         ==> Represents disjoint sets that represent the forest.
                                i.e each tree in forest belongs to a disjoint set

        degree              ==> contains a mapping from vertex --> its degree
                                degree[k] is vertex k's degree
        -------------------------------------------------------------------------
        """

        # init variables
        vertex_sets = util.disjointSets(range(input_graph.num_nodes))
        degree = [0] * input_graph.num_nodes
        forest_edge_set = set()

        #graph_stats = input_graph.stats()
        #branch_threshold = graph_stats["average_degree"]
        #print "branch_threshold: %s" %(str(branch_threshold))

        for v in range(input_graph.num_nodes):
            S_prime = ([],[])
            d_prime = 0
            for u in input_graph.neighbors[v]:
                if vertex_sets.find(u) != vertex_sets.find(v) and vertex_sets.find(u) not in S_prime[1]:
                    d_prime += 1
                    S_prime[0].append(u)
                    S_prime[1].append(vertex_sets.find(u))
            if degree[v] + d_prime >= branch_threshold:
                for u in S_prime[0]:
                    forest_edge_set.add(Edge(u,v))
                    vertex_sets.union(u,v)
                    degree[u] += 1
                    degree[v] += 1

        return forest_edge_set, vertex_sets, degree

    def score(self,edge,degrees):
        """
        Score = How badly the edge should be added.
        If score = 3, the edge must be added cuz its sooo good
        ---------------------------------------------------------------
        Score 3 ==> Edge connects a Fat ass node (node with >1 degree)
                    to a singleton. This is a good edge

        Score 2 ==> Both Nodes of edge are Fat, so this edge doesn't 
                    hurt, but still isn't bad

        Score 1 ==> One of the Nodes is Fat, But the other one
                    is a leaf. This sucks, because the leaf will loose
                    its pristine status

        Score 0 ==> They are both leaves :( ARGHHHHHHHHHHHHHHH
        ---------------------------------------------------------------
        """
        scr = 0

        # Case 1: when edge connects a FAT node to a singleton
        # This edge can definitely be added because the FAT node
        # cant be a leaf anyways, and the singleton becomes a leaf
        if degrees[edge[0]] == 0 and degrees[edge[1]] > 1: return 3
        elif degrees[edge[1]] == 0 and degrees[edge[0]] > 1: return 3

        # Else: We generally want to add the edge when the nodes of the edge
        # can't possibly be leaves.
        # Higher degree = higher score
        if degrees[edge[0]] > 1: scr += 1
        if degrees[edge[1]] > 1: scr += 1
        return scr
    
def experiment(edge_set, mlst_handler, experiment_name="Experiment:", experiment_desc=None, display=False):
    """
    Runs the experiment with a given handler and edge set
    """

    # run the experiment
    print ">>> %s" %(str(experiment_name)); stime = time.time()
    print "--------------------------------------------------------------"

    output_edge_set = mlst_handler.find_mlst(edge_set)

    print "--------------------------------------------------------------"

    etime = time.time(); duration = int((etime - stime) * 1000)
    output_graph = graph.make_graph(output_edge_set)
    output_graph.search()
    stats = output_graph.stats()

    print ">>> Average Degree: %s" %(str(stats["average_degree"]))
    print ">>> Number of Leaves: %s" %(str(output_graph.num_leaves))
    print "<<< Time Elapsed: %d ms" %(duration)
    print "\n"

    # display input/output graph
    if display: util.display(edge_set)
    if display: util.display(output_edge_set)

    stats = {}
    stats["duration"] = duration
    stats["output_edge_set"] = output_edge_set
    return stats
    
if __name__ == "__main__":   
    # create handlers
    mlst_handler = {}
    mlst_handler["ConstantTimeMLST"] = ConstantTimeMLST()
    mlst_handler["BruteforceMLST"] = BruteforceMLST()
    print ""

    # Experiment 1
    # ---------------------------------------------------------------------------------------
    edgeSet = set()
    for i in range(100):
        for n in range(i+1,100):
            edgeSet.add(Edge(i,n))
    stats = experiment(edge_set=edgeSet, mlst_handler=mlst_handler["ConstantTimeMLST"],
            experiment_name="Experiment 1: Everything to Everything graph", 
            display=False)
    # ---------------------------------------------------------------------------------------

    # Experiment 2
    # ---------------------------------------------------------------------------------------
    edgeSet = set() 
    for i in range(98):
        edgeSet.add(Edge(i+1,i))
    edgeSet.add(Edge(1,99))
    stats = experiment(edge_set=edgeSet, mlst_handler=mlst_handler["ConstantTimeMLST"],
            experiment_name="Experiment 2: Linear Linked List", 
            display=False)
    # ---------------------------------------------------------------------------------------

    # Experiment 3
    # ---------------------------------------------------------------------------------------
    edgeSet = set() 
    for i in range(97):
        edgeSet.add(Edge(i+1,i))
    edgeSet.add(Edge(1,99))
    edgeSet.add(Edge(1,98))
    edgeSet.add(Edge(98,99))
    stats = experiment(edge_set=edgeSet, mlst_handler=mlst_handler["ConstantTimeMLST"],
            experiment_name="Experiment 3: Linked List with annoying Cycle at the end", 
            display=False)
    # ---------------------------------------------------------------------------------------

    # Experiment 4
    # ---------------------------------------------------------------------------------------
    nbit_generator = nbit.NbitGenerator(100,3)
    edgeSet = nbit_generator.generate_graph()
    stats = experiment(edge_set=edgeSet, mlst_handler=mlst_handler["ConstantTimeMLST"],
            experiment_name="Experiment 4: Nbic Graph Fun", 
            display=False)
    # ---------------------------------------------------------------------------------------


