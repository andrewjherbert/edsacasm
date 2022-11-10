# Reverse an SSI input file

import sys

line = sys.stdin.readline()
while line:
    line = line[:-1]
    #print(line)
    print(line[::-1])
    line = sys.stdin.readline()
