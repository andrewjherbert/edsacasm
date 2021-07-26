# EDSAC Test Program Assembler - Andrew Herbert - 25 July 2021

# Generates binary images for loading into the bottom EDSAC store tank
# (locations 0-63) using Tom Toth's SSI unit.


# Usage: edsacasm.py [-h] [-list] [-infile INFILE] [-outfile OUTFILE]

# Syntax
#
# <program> = <line> [<line>*]
# <line> = [<label>] []<word>] [comment]
# <label> = .<name>.
# <name> = alpha numeric sequence
# <word> = <number> | <order>
# <number> = +<digits> | -<digits> | &<digits> | B<binary digits>
# <order> = <function letter> []<address>] F | <function letter> <address> D
# <address> = <integer> | <label>
# <comment> = ; text terminated by newline

import sys
import os.path
import argparse

# ---- Global variables ---- #

inFilePath = ""
outFilepath = ""
#listFilePath = ""
list = False

store = [ 0 for x in range(64)] # store image
cpa = 0 # current placing aqddress
lineNo = 1
lineStart = 0

symbols = dict() # symbol table

functionCodes = "P~~ERTYUIO~~SZ~~~F~~~HN~~LXGA~C~"

# ---- assembler ---- #

def assembler():

    global cpa

    #print("***Assembler")

    # Open input
    if inFilePath == "":
        inFile = sys.stdin.read()
    else:
        try:
            inFile = open(inFilePath, 'rt').read()
        except:
            fail("Cannot open input")
            sys.exit(1)
    inFile = inFile + "\n" # ensure terminated by a newline

    # Open output
    if outFilePath == "":
        outFile = sys.stdout
    else:
        try:
            outFile = open(outFilePath, 'wt')
        except:
            fail("Cannot open output")

    #print("Input is:\n", inFile, "\nLength =", len(inFile))

    # First pass
    cpa = 0 # assemble from location 0 onwards
    assemble(inFile, 0, 1)

    # Second pass
    cpa = 0
    assemble(inFile, 0, 2)

    # Dump out content of store
    if list:
        listStore(outFile)
    else:
        dumpStore(outFile)

# ---- assemble ---- #

def assemble(f, i, p): # assemble next line if any
    #print("***Assemble", i, p)
    if cpa > 63:
        syntaxError(f, "program extends beyond tank 0")
    while i < len(f):
        i = skipSpace(f, i)
        if f[i] == '\n':
            i = newline(f, i)
        elif f[i] == ';':
            i = comment(f, i+1)
        elif f[i] == '.':
            i = labelDef(f, i+1, p)
        elif f[i] == '+' or f[i] == '-':
            i = number(f, i)
        elif f[i] == '&':
            i = octal(f, i)
        elif f[i] == 'B':
            i = binary(f, i)
        elif f[i].isalpha():
            i = order(f, i, p)
        else:
            syntaxError(f, "Unexpected symbol '" + f[i] + "'")

# ---- comment ---- #

def comment(f, i): # assemble comment
    #print("***Comment", i, '"', f[i], '"');
    while f[i] != '\n':
        i+= 1
    return i

# ---- labelDef ---- #

def labelDef(f, i, p): # assemble label definition
    global symbols
    i, name = label(f, i, p)
    symbols[name] = cpa
    return i

# ---- label ---- #

def label(f, i, p): # assemble label
    #print("***Label", i, '"', f[i], '"')
    j = i+1
    while f[j] != '.':
        if f[j] == '\n':
            syntaxError(f, "malformed label")
        else:
             j += 1
    name = f[i:j]
    return (j+1, name)

 # ---- number ---- #

def number(f, i):
    global cpa, store
    #print("***Number", i, '"', f[i], '"')
    j = i+1
    while f[j].isdigit():
        j += 1
    value = int(f[i:j])
    if value < -65536 or value > 65535:
        syntaxError(f, "number greater than 17 bits long")
    store[cpa] = value
    #print("***Result =", value)
    cpa += 1
    return j

# ---- octal ---- #

def octal(f, i):
    global cpa, store
    i += 1 # skip over &
    value = 0
    digits = 0
    while f[i].isdigit():
        if f[i] == '9':
            digits += 1
            value = (value << 1) + 1
        elif f[i] == '8':
            digits += 1
            value = (value << 1)
        else:
            digits += 1
            value = (value << 3) +(ord(f[i])-ord('0'))
        if value >= 65536:
            syntaxError(f, "octal greater than 17 bits long")
        i += 1 # move to next digit
    if digits == 0:
        syntaxError(f, "no digits found after &")
    store[cpa] = value
    cpa += 1
    return i

# ----binary ---- #

def binary(f, i):
    global cpa, store
    i += 1 # skip over B
    digits = 0
    value = 0
    while True:
        if f[i] == '0':
            value = value << 1
            digits += 1
            i += 1
        elif f[i] == '1':
            digits += 1
            i += 1
            value = (value << 1) +1
            if value >= 65536:
                syntaxError(f, "binary larger than 17 bits long")
        elif digits == 0:
            syntaxError(f, "no digits found after B")
        else:
            store[cpa] = value
            cpa += 1
            return i

# ---- order ---- #

def order(f, i, p):
    global cpa, store, functions
    #print("***Order", i, '"', f[i], '"')
    order = functionCodes.find(f[i])
    store[cpa] = order << 12
    if order == -1:
        syntaxError(f, "function code expected")
    i = address(f, i+1, p)
    i = skipSpace(f, i)
    if f[i] == 'F':
        long = 0
    elif f[i] == 'D':
        long = 1
    else:
        syntaxError(f, "F or D expected")
    store[cpa] += long
    cpa +=1
    return i+1

# ---- address ---- #

def address(f, i, p):
    global cpa, store, symbols
    #print("Address", i, '"', f[i], '"')
    i = skipSpace(f, i)
    if f[i].isdigit():
        j = i+1
        while f[j].isdigit():
            j += 1
        addr = int(f[i:j])
        if addr > 1023:
            syntaxError(f, "address field too large")
        store[cpa] += (addr << 1)
        #print("***Result =", addr)
        return j
    elif f[i] == '.':
        j, name = label(f, i+1, p)
        #print("***Result =", name, p)
        if p == 2:
            if name in symbols:
                #print(name, "found")
                store[cpa] += (symbols[name] << 1)
            else:
                syntaxError(f, "undefined label - " + name)
        return j
    else:
        #print("***Result =", 0)
        return i

# ---- newline ---- #

def newline(f, i):
    global lineNo, lineStart
    print("***Newline", lineNo, f[lineStart:i]);
    lineNo += 1
    lineStart = i+1
    return lineStart

# ---- skipSpace ---- #

def skipSpace(f, i):
    #print("***SkipSpace", i)
    if f[i] == ' ' or f[i] == "\t":
        return skipSpace(f, i+1)
    else:
        return i

# ---- syntaxError ---- #

def syntaxError(f, reason):
    global lineNo, lineStart
    msg = "Syntax error in line " + str(lineNo) + ": " + reason + '\n'
    lineEnd = f.index('\n', lineStart)
    msg = msg + f[lineStart:lineEnd-1]
    fail(msg)

 # ---- dumpStore, listStore ---- #

def dumpStore(f):
    #print("***Dumping store")
    global cpa, store
    for i in range(64):
        bits = '0'+format(store[i], "017b")[::-1]
        f.write(bits)
        f.write('\n')

def listStore(f):
    #print("***Listing store")
    global cpa, store
    for i in range(64):
        f.write("%2d " % i)
        bits = '0' + format(store[i], "017b")[::-1]
        f.write(bits)
        fn = functionCodes[store[i] >> 12]
        ad = str((store[i] >> 1) & 1023)
        lg = "D" if (store[i] & 1 == 1) else "F"
        f.write("    " + fn + ad + lg + '\n')

# ---- Error handling ---- #

def fail(msg):
    sys.stderr.write(msg)
    sys.exit(1)

# ---- Decode arguments ---- #

def getArgs():
    global inFilePath, outFilePath, listFilePath, list
    parser = argparse.ArgumentParser(
            description='Simple EDSAC assembler for test programs')
    parser.add_argument('-list', action='store_true')
    #parser.add_argument('-listfile', help='output program listing', default='')
    parser.add_argument('-infile',  help='input file', default='')
    parser.add_argument('-outfile',  help='output file', default='')
    args = parser.parse_args()
    inFilePath = args.infile
    outFilePath = args.outfile
    #listFilePath = args.listfile
    list = args.list

# ---- Main program ---- #

getArgs()
#print("***In=", inFilePath, "Out=", outFilePath)
assembler()
