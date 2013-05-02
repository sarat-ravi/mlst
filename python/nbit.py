#!/usr/bin/env python
import sys
import os
import getopt

import reader
import util
import graph
from mlst import (BruteforceMLST)

class NbitGenerator:
    def __init__(self, max_nodes, degree):
        self.degree = degree
        self.max_nodes = max_nodes

        # initialize edges to be the "base cubit"
        self.base_edges = [
                graph.Edge(0, 1),
                graph.Edge(0, 2),
                graph.Edge(0, 3),
                graph.Edge(1, 2),
                graph.Edge(1, 3),
                graph.Edge(2, 3)
                ]
        self.base_edges = set(self.base_edges)
        self.edges = self.base_edges.copy()

        initial_num_vertices = 4

        self.initial_num_vertices = initial_num_vertices 
        self.num_vertices = initial_num_vertices

        self.graph = graph.make_graph(self.edges)
        self.graph.search()

    def get_touching_edges(self, vertex, neighbors):
        """
        returns all edges involved with <vertex> and its <neighbors>
        """

        return [graph.Edge(vertex, n) for n in neighbors]

    def replace(self, vertex, edges_to_modify, vertices_to_add):
        """
        modify edges to discard vertex and point to a new vertex instead
        """
        assert len(edges_to_modify) == len(vertices_to_add), "The lengths don't match!!"

        new_edges = []
        for edge, new_vertex in zip(edges_to_modify, vertices_to_add):
            
            new_pair = []
            for a in edge.ends:
                if a == vertex:
                    continue
                new_pair.append(a)

            new_pair.append(new_vertex)

            assert len(new_pair) == 2, "The edge %s doesn't contain vertex %s!!" %(str(edge),
                    str(vertex))
            
            a, b = new_pair
            new_edge = graph.Edge(a, b)
            new_edges.append(new_edge)

        return new_edges

    def update_graph(self):
        self.graph = graph.make_graph(self.edges)
        self.graph.search()

    def expand(self, vertex=0):
        """
        expands <vertex> into 3
        """
        self.update_graph()

        neighbors = self.graph.neighbors[vertex]
        touching_edges = self.get_touching_edges(vertex, neighbors)

        # these edges will be pointing to new stuff
        edges_to_modify = touching_edges[1:]
        try:
            for edge in edges_to_modify:
                self.edges.remove(edge)
        except KeyError, e:
            import IPython; IPython.embed()


        #vertices_to_add = [self.num_vertices + 1, self.num_vertices + 2]
        vertices_to_add = [self.num_vertices + i for i in range(0, self.degree-1)]
        self.num_vertices += self.degree - 1

        # link these new vertices together
        for new_vertex in vertices_to_add:
            new_edge = graph.Edge(new_vertex, vertex)
            self.edges.add(new_edge)

        # TODO: make this more generic
        another_edge = graph.Edge(vertices_to_add[0], vertices_to_add[1])
        self.edges.add(another_edge)

        modified_edges = self.replace(vertex, edges_to_modify, vertices_to_add)

        # add it back to set
        for edge in modified_edges:
            self.edges.add(edge)

        #import IPython; IPython.embed()

    def generate_graph(self):
        """
        The main function, generates the edge_set for an n-bit, k-node graph
        """
        # see how many times we have to call expand
        num_expand_iterations = (self.max_nodes - self.initial_num_vertices) / (self.degree - 1)

        # call expand that many times, expanding a node into degree - 1 new nodes + this node
        for i in range(num_expand_iterations):
            self.expand(vertex=0)

        # in case the graph is stale, update it once more
        self.update_graph()
        return self.edges

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
    #util.display(edge_set)

    # generates 
    edge_set = nbit_generator.generate_graph()
    #util.display(edge_set)

    # make sure that the degree is the same
    for i in range(nbit_generator.num_vertices):
        neighbors = nbit_generator.graph.neighbors[i]
        assert len(neighbors) == nbit_generator.degree, "neighbors are not all %d!!" %(nbit_generator.degree)
    
    # print 
    num_nodes = nbit_generator.num_vertices

    print "Graph Stats:"
    print "------------------------------------------------"
    print "Number of nodes: %d" %(num_nodes)
    print "%d node %d-bit Graph Generated" %(num_nodes, nbit_generator.degree)
    print "------------------------------------------------\n"

    return edge_set

if __name__ == "__main__":

    # get cli args
    args = get_args()
    output_filename = args["output_filename"]

    # graphs to generate
    nbit_generators = [
            NbitGenerator(max_nodes=10, degree=3),
            NbitGenerator(max_nodes=100, degree=3),
            ]

    # write edge sets to file
    edge_sets = map(generate_nbit_graph, nbit_generators)
    util.write_output_to_file(edge_sets, output_filename)
    print "Edge Sets written to file '%s'" %(str(output_filename))


