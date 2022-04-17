import sys
import os.path
from GrammarParser import GrammarParser

if len(sys.argv) <2:
    print("Must pass input file as argument.")
    sys.exit(1)

file = sys.argv[1]

if not os.path.isfile(file):
    print("Input file does not exist.")
    sys.exit(1)

outfile = file + ".out"

output = GrammarParser(file).parse_grammar()

with open(outfile, "w") as f:
        for element in output:
            f.write(element + "\n" + str(output[element]) + "\n")

    