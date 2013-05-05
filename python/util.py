#!/usr/bin/env python
import sys
import reader

def print_error(err):
    sys.stderr.write(err)

def print_message(msg):
    sys.stdout.write(msg)

def get_input_edge_sets(infile):
    """
    like checker.check_input(), reads from file and returns edge_sets
    """
    edge_sets = None
    try:
        f = open(infile)
        in_reader = reader.InFileReader(f)
        edge_sets = in_reader.read_input_file()
        print_message("Input file '{0}' has the correct format.\n".format(infile))

    except IOError as e:
        print_error("Error reading '{0}' ({1}).\n".format(infile, e))
    except reader.ReaderException as e:
        print_error("({0}) {1}\n".format(infile, e))

    return edge_sets

def is_mlst(edge_set):
    """
    Get number of leaves if graph is mlst
    else return False
    """
    import graph
    graph = graph.make_graph(edge_set)
    graph.search()
    return graph.num_leaves if (graph.edges_in_one_component() and len(graph.get_edge_set()) == (graph.num_nodes - 1) and not graph.has_cycle) else False

def write_output_to_file(edgesets,filename):
    """
    like checker.check_input(), reads from file and returns edge_sets
    """
    #TODO: implement this
    #NOTE: comment out line below
    f=open(filename,"w")
    daINT=len(edgesets)
    f.write(str(daINT)+"\n")
    for edgeset in edgesets:
        lolz=len(edgeset)
        f.write(str(lolz)+"\n")
        for edge in edgeset:
            f.write(str(edge.ends[0])+" "+str(edge.ends[1])+"\n")

def display(input_edge_set):
    from igraph import *
    """
    displays a graph, given the edge set
    """
    g = Graph()

    # format and add edges to graph
    edges = [tuple(e.ends) for e in input_edge_set]
    vertices = list(set([v for e in edges for v in e]))

    vertex_id = {}
    count = 0
    for v in vertices:
        vertex_id[v] = count
        count += 1

    # construct graph
    g.add_vertices(len(vertices))
    for a, b in edges: g.add_edge(vertex_id[a], vertex_id[b])

    # name the vertices
    g.vs["name"] = [v for v in vertex_id.keys()]

    # plot it
    layout = g.layout("kk")
    plot(g, layout = layout)



class disjointSets():
    def __init__(self,lst):
        self.mappings = dict(zip(lst,range(len(lst))))
        self.sizes = [1 for item in lst]
        self.items = lst[:]
        self.sets = [[item] for item in lst]
        self.numSets = len(lst)

    def find(self,item):
        ind = self.mappings[item]
        while ind != self.mappings[self.items[ind]]:
            self.mappings[self.items[ind]] = self.mappings[self.items[self.mappings[self.items[ind]]]]
            ind = self.mappings[self.items[ind]]
        return self.items[ind]

    def size(self,item):
        return self.sizes[self.mappings[self.find(item)]]

    def addSet(self,identifier):
        self.mappings[identifier] = len(self.items)
        self.sizes.append(1)
        self.items.append(identifier)
        self.sets.append([identifier])

    def union(self,a,b):
        (big, little) = (a,b) if self.size(a) > self.size(b) else (b,a)
        littleSize = self.size(little)
        bigParent,littleParent = self.find(big), self.find(little)
        assert bigParent != littleParent, "bigParent = littleParent = %d" % bigParent
        self.sets[self.mappings[bigParent]] += self.sets[self.mappings[littleParent]]
        self.mappings[littleParent] = self.mappings[bigParent]
        self.sizes[self.mappings[bigParent]] += littleSize
        self.numSets -= 1

    def getSet(self, item):
        return self.sets[self.mappings[self.find(item)]]

    def display(self):
        print"==============="
        print "MAPPINGS: ", self.mappings
        print "sizes: ", self.sizes
        print "items: ", self.items
        print"==============="
