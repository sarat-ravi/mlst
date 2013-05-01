import graph


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

    def display(self, input_edge_set):
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

        try:
            # construct graph
            g.add_vertices(len(vertices))
            for a, b in edges:
                g.add_edge(vertex_id[a], vertex_id[b])
        except:
            import IPython; IPython.embed() 

        # plot it
        layout = g.layout("kk")
        plot(g, layout = layout)

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
