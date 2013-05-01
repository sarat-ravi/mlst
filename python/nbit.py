#!/usr/bin/env python

import reader
import util
import graph

class CubitGenerator:
    def __init__(self, max_nodes):
        self.degree = 3
        self.max_nodes = max_nodes

        # initialize edges to be the "base cubit"
        self.edges = [
                graph.Edge(0, 1),
                graph.Edge(0, 2),
                graph.Edge(0, 3),
                graph.Edge(1, 2),
                graph.Edge(1, 3),
                graph.Edge(2, 3)
                ]
        self.edges = set(self.edges)

        self.num_vertices = 4

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

if __name__ == "__main__":

    cubit_generator = CubitGenerator(3)

    # before
    #edge_set = cubit_generator.edges
    #util.display(edge_set)

    # expand vertex 0 to "triplify"
    for i in range(48):
        cubit_generator.expand(vertex=0)

    # make sure stale data gets deleted
    cubit_generator.update_graph()

    # after
    edge_set = cubit_generator.edges
    #util.display(edge_set)

    # make sure that the degree is the same
    degree = 3
    for i in range(cubit_generator.num_vertices):
        neighbors = cubit_generator.graph.neighbors[i]
        assert len(neighbors) == degree, "neighbors are not all 3!!"

    print "Number of nodes: %d" %(cubit_generator.num_vertices)
    print "100 node Cubit generated!!"






        

