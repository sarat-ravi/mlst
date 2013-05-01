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
    print g.vs["name"]

    # plot it
    layout = g.layout("kk")
    plot(g, layout = layout)




