#!/usr/bin/env python
import os
import sys
import getopt
import datetime
import time
import shlex
import shutil
from mlst import *
from pprint import pprint

import reader
import util

from mlst import (MLST, 
        BullshitMLST,
        BruteforceMLST,
        )

"""
This code reads in the input file, does stuff to it,
and writes a graph to the output file
"""

def get_args():
    def usage():
        print "Command Line Interface for MLST\n"
        print "SAMPLE USAGE: ./setup.py -i <inputfile> -o <outputfile>"
        print "Ex: ./setup.py -i blah.in -o blah.out\n"
        print "-i <input_file> (default=mlst.in)"
        print "-o <output_file> (default=mlst.out)"
        print ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:h", ["input=", "output=", "help"])
    except:
        usage()
        exit()

    # init defaults
    input_file = None
    output_file = "mlst.out"

    # parse cli args
    for o,a in opts:
        if o in ("-i", "--input"):
            input_file = a 
        if o in ("-o", "--output"):
            output_file = a 
        elif o in ("-h", "--help"):
            usage()
            exit()

    # complain if input not specified
    if not input_file:
        usage()
        exit()

    # check validity
    assert os.path.exists(input_file), "Input File %s doesn't exist" %(str(input_file))
    output_dirname = os.path.dirname(output_file)
    if output_dirname == '': output_dirname = "."
    assert os.path.exists(output_dirname), "Output Directory %s doesn't exist" %(str(input_file))

    # return final result
    result = {}
    result["input_filename"] = input_file
    result["output_filename"] = output_file
    return result


def find_mlst(edge_set, MlstHandler):
    """
    takes an edge_set, and returns result_edge_set
    """
    # set MLST runner
    mlst_handler = MlstHandler()


    # get output
    output_edge_set = mlst_handler.find_mlst(edge_set)

    """
    draw the graph
    you need to install igraph and py-cairo module
    py-cairo can be installed by "sudo port install py-cairo"
    """
    #util.display(output_edge_set)
    return output_edge_set

if __name__ == "__main__":

    # create file objs from command line args
    args = get_args()

    # get input edges
    input_edge_sets = util.get_input_edge_sets(infile=args["input_filename"])

    output_edge_sets = []
    for edge_set in input_edge_sets:
        #output_edge_sets.append(find_mlst(edge_set=edge_set, MlstHandler=BruteforceMLST))
        output_edge_sets.append(find_mlst(edge_set=edge_set, MlstHandler=ConstantTimeMLST))

    # write output to file
    util.write_output_to_file(output_edge_sets,filename=args["output_filename"])


