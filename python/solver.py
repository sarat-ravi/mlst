#!/usr/bin/env python
import sys
import os
import getopt

import reader
import util
import graph
from mlst import (BruteforceMLST)
from nbit import NbitGenerator

class NbitConstructor:
    def __init__(self, max_nodes, degree):
        self.degree = degree
        self.max_nodes = max_nodes

        self.edges = set(self.get_star(0, range(1,degree+1)))
        self.base_edges = self.edges.copy()

        self.num_vertices = self.degree + 1 

        self.graph = graph.make_graph(self.edges)
        self.graph.search()

        self.nbg = NbitGenerator(max_nodes, degree)

    def get_star(self, vertex, neighbors):
        """
        returns all edges involved with <vertex> and its <neighbors>
        """

        return [graph.Edge(vertex, n) for n in neighbors]

    def update_graph(self):
        self.graph = graph.make_graph(self.edges)
        self.graph.search()

    def get_leaves(self):
        leaves = set()
        for v in range(self.num_vertices):
            n = len(self.graph.neighbors[v])
            if n == 1: leaves.add(v)

        return leaves

    def generate_graph(self):

        self.update_graph() 

        leaves = self.get_leaves()

        while self.num_vertices < self.max_nodes - (self.degree - 1):
            leaf = leaves.pop()

            self.nbg.expand(leaf)

            vertices_to_add = [self.num_vertices + i for i in range(0, self.degree-1)]
            new_edges = self.get_star(leaf, vertices_to_add)

            # update state
            self.num_vertices += self.degree - 1
            for e in new_edges: self.edges.add(e)
            for v in vertices_to_add: leaves.add(v)

        return self.nbg.edges, self.edges


def get_args():
    def usage():
        print "Command Line Interface for Nbit Graph Generator\n"
        print "SAMPLE USAGE: ./nbit.py <outfile>"
        print "Ex: ./nbit.py blah.out\n"
        print ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
        output_file = args[0] 
    except:
        usage()
        exit()

    # parse cli args
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
            exit()

    # check validity
    output_dirname = os.path.dirname(output_file)
    if output_dirname == '': output_dirname = "."
    assert os.path.exists(output_dirname), "Output Directory %s doesn't exist" %(str(input_file))

    # return final result
    result = {}
    result["output_filename"] = output_file
    return result

def generate_nbit_graph(nbit_generator):

    # before
    base_edge_set = nbit_generator.base_edges
    #util.display(base_edge_set)

    # generates 
    original_edge_set, mlst_edge_set = nbit_generator.generate_graph()
    util.display(mlst_edge_set)
    util.display(original_edge_set)

    # make sure that the degree is the same
    #for i in range(nbit_generator.num_vertices):
        #neighbors = nbit_generator.graph.neighbors[i]
        #assert len(neighbors) == nbit_generator.degree, "neighbors are not all %d!!" %(nbit_generator.degree)
    
    return original_edge_set, mlst_edge_set 

if __name__ == "__main__":

    # get cli args
    args = get_args()
    output_filename = args["output_filename"]
    # -----------------------------------------------------------------------

    """
    NOTE: Modify this list to add/remove/change generators
    """
    # graphs to generate
    nbit_generators = [
            NbitConstructor(max_nodes=100, degree=3),
            NbitConstructor(max_nodes=98, degree=33),
            NbitConstructor(max_nodes=10, degree=3),
            ]

    # -----------------------------------------------------------------------
    # write edge sets to file
    #edge_sets = map(generate_nbit_graph, nbit_generators)
    mlst_edge_sets = []
    orig_edge_sets = []

    for nbit_generator in nbit_generators:
        orig, mlst = generate_nbit_graph(nbit_generator)
        mlst_edge_sets.append(mlst)
        orig_edge_sets.append(orig)

    orig_filename = "hard.in"
    mlst_filename = "hard.out"
    util.write_output_to_file(orig_edge_sets, orig_filename)
    util.write_output_to_file(mlst_edge_sets, mlst_filename)

    print "Orig Edge Sets written to file '%s'" %(str(orig_filename))
    print "Mlst Edge Sets written to file '%s'" %(str(mlst_filename))


