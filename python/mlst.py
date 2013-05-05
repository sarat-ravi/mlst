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
    def find_mlst(self, edge_set):
        input_graph = graph.make_graph(edge_set)
        input_graph.search()
        leafyForest, vertexSets, degrees = self.find_leafyForest(input_graph)

        ideal_scores = (3,2)
        nonideal_scores = (1,0)
        while vertexSets.numSets > 1:
            goodEdges = {0:[],1:[],2:[],3:[]}
            for edge in input_graph.edges:
                if vertexSets.find(edge[0]) != vertexSets.find(edge[1]):
                    scr = self.score(edge,degrees)
                    goodEdges[scr].append(edge)
            for score in ideal_scores:
                for edge in goodEdges[score]:  #first, try to add every edge which, when added, keeps all leaves
                    if vertexSets.find(edge[0]) != vertexSets.find(edge[1]):
                        leafyForest.append(Edge(edge[0],edge[1]))
                        vertexSets.union(edge[0],edge[1])
            added_nonideal_edge = False
            for score in nonideal_scores:  #count down by score
                for edge in goodEdges[score]:
                    if not added_nonideal_edge:   # 
                        leafyForest.append(Edge(edge[0],edge[1]))
                        vertexSets.union(edge[0],edge[1])
                        added_nonideal_edge = True
                    else: break
        return set(leafyForest)
        
    def score(self,edge,degrees):
        scr = 0
        if degrees[edge[0]] == 0 and degrees[edge[1]] > 1:
            scr = 3
            return scr
        elif degrees[edge[1]] == 0 and degrees[edge[0]] > 1:
            scr = 3
            return scr
        if degrees[edge[0]] > 1:
            scr += 1
        if degrees[edge[1]] > 1:
            scr += 1
        return scr
            
    def find_leafyForest(self, input_graph):
        vertexSets = util.disjointSets(range(input_graph.num_nodes))
        d = [0] * input_graph.num_nodes
        F = []
        for v in range(input_graph.num_nodes):
            S_prime = ([],[])
            d_prime = 0
            for u in input_graph.neighbors[v]:
                if vertexSets.find(u) != vertexSets.find(v) and vertexSets.find(u) not in S_prime[1]:
                    d_prime += 1
                    S_prime[0].append(u)
                    S_prime[1].append(vertexSets.find(u))
            if d[v] + d_prime >= 3:
                for u in S_prime[0]:
                    F.append(Edge(u,v))
                    vertexSets.union(u,v)
                    d[u] += 1
                    d[v] += 1
        return F, vertexSets, d
    
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
            experiment_name="Experiment 4: Cubic Graph Fun", 
            display=False)
    # ---------------------------------------------------------------------------------------


