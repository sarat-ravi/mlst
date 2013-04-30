MLST
========

## Getting Started
### Overview
Important Files:

* #####main.py (driver)
* #####mlst.py (where the actual algo goes)

###Main.py


main.py serves as the driver class, and deals with parsing the right command line args. It gets ```edge_sets``` from the input graph file and sends it to mlst.py, which processes it in some way and returns ```result_edge_sets``` which main.py writes to the output file.

###mlst.py

mlst.py has classes that represent different implementations to solve the MLST problem. Each of these handlers are required to inherit the base ```MLST``` class interface.

### Usage:
```
$ ./main.py -i <input_file> -o <output_file>
```
* NOTE: the ```<output_file>``` will be created if it doesn't already exists, as long as the directory is valid


## Format Checkers 

version: 1

This directory contains the Python implementations of the format checkers.
Our submission system will be implemented using the Go format checkers, but
for checking formats the Python implementations should be sufficient.

===== To use the format checkers =====

If you have Python installed, run
  $ python check_input.py
or
  $ python check_input.py file.in

The first command checks the default input file (i.e., "mlst.in"), and the
second command checks the input file "file.in".

To check the output file, run:
  $ python check_output.py
or
  $ python check_output.py file.in file.out

The first command checks the default output file (i.e., "mlst.out") against
the default input file (i.e., "mlst.in").
The second command checks the output file "file.out" against the input file
"file.in".

See config.py for the default settings.
