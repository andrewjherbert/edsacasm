# EDSAC Test Program Assembler - Andrew Herbert -15 February 2022

# Generates binary images for loading into the bottom EDSAC store tank
# (locations 0-63) using Tom Toth's SSI unit.


# Usage: edsacasm.py infile|- [-h] [-list] [-o/--out=output-file] [-t/-tanks=nnn]
# -list option produces annotated output.  Without -list output is suitable for
# loading via ssiupload. -tanks specified maximum number of main store tanks
# (32 words each) available.

# Syntax
#
# <program> = <item> [<item>*]
# <line> = [@] [<label>]* [<word>] [comment]
# <label> = .<name>.
# <name> = alpha numeric sequence
# <word> = <number> | <order>
# <number> = +<digits> | -<digits> | &<digits> | B<binary digits> | <number>L
# <order> = <function letter> [<address>] F | <function letter> <address> D
# <address> = <integer> | <label>
# <comment> = ; text terminated by newline

# @ forces next word to be aligned to even address

# Numbers and orders are stored as short numbers (17 bits) ubless followed by L in 
# which case they are assembled as 35 bit long numbers in the next two succeeding
# locations.  The @ symbol should be used befoe the label to foce alignment on a
# even address.

import sys
import os.path
import argparse

# ---- Global variables ---- #

inFilePath  = ""
outFilePath = ""
list = False

store = []  # store image in hardware (36 bit) form - size set in getargs

cpa = 0 # current placing address
lineNo = 1
lineStart = 0

symbols = dict() # symbol table

functionCodes = "PQWERTYUIOJ#SZK*.FhD!HNM&LXGABCV"

# ---- assembler ---- #

def assembler():
    global cpa

    outfile = None

    #print("***Assembler")

    # Open input
    if inFilePath == "-":
        inFile = sys.stdin.read()
    else:
        try:
            inFile = open(inFilePath, 'rt', encoding='utf-8-sig').read()
        except:
            fail("Cannot open input")
            sys.exit(1)
    inFile = inFile + "\n" # ensure terminated by a newline

    # Open output
    if outFilePath == '-':
        outFile = sys.stdout
    else:
        try:
            outFile = open(outFilePath, 'wt', encoding='ascii')
        except:
            fail("Cannot open output")
            sys.exit(1)

    # First pass
    cpa = 0 # assemble from location 0 onwards
    assemble(inFile, 0, 1)

    # Second pass
    cpa = 0
    assemble(inFile, 0, 2)

    # Dump out content of store
    if list:
        dumpStore(outFile, True)
    else:
        dumpStore(outFile, False)

# ---- assemble ---- #

def assemble(f, i, p): # assemble next line if any
    global cpa
    #print("***Assemble", i, p)
    if cpa > 31:
        syntaxError(f, "program extends beyond tank 0")
    while i < len(f):
        i = skipSpace(f, i)
        if f[i] == '\n':
            i = newline(f, i)
        elif f[i] == ';':
            i = comment(f, i+1)
        elif f[i] == '@':
            i = align(f, i, p)
        else:
            i = labelledWord (f, i, p)

# ---- comment ---- #

def comment(f, i): # assemble comment
    #print("***Comment", i, '"', f[i], '"');
    while f[i] != '\n':
        i += 1
    return i

# ---- align ---- #

def align(f, i, p): # align on even word
    global cpa
    #print("Align", i, p)
    if (cpa&1) == 1:
        cpa +=1
    i += 1
    if i < len(f):
        i = labelledWord(f, i, p)
    return i

# ---- labels ---- #

def labelledWord(f, i, p):
    #print("***labelledWord", i, p)
    # look for labels
    i = skipSpace(f, i)
    while f[i] == '.':
        i = labelDef(f, i+1, p)
        i = skipSpace(f, i)
        # look for word
    if f[i] == '+' or f[i] == '-':
        return number(f, i)
    elif f[i] == '&':
        return octal(f, i)
    elif f[i] == 'B':
        return binary(f, i)
    elif f[i].isalpha():
        return order(f, i, p)
    elif f[i] == '\n':
        return newline(f, i)
    else:
        syntaxError(f, "Unexpected symbol '{}' ({})".format(f[i], ord(f[i])))
    
# ---- labelDef ---- #

def labelDef(f, i, p): # assemble label definition
    global symbols
    #print("***labelDef", i, p);
    i, name = label(f, i, p)
    if   p == 1 and name in symbols:
        syntaxError(f, "Label already defined")
    symbols[name] = cpa
    return i

# ---- label ---- #

def label(f, i, p): # assemble label
    #print("***Label", p, i, '"', f[i], '"')
    j = i+1
    while f[j] != '.':
        if f[j] == '\n':
            syntaxError(f, "malformed label")
        else:
             j += 1
    name = f[i:j]
    #print("Name:", name)
    return (j+1, name)

 # ---- number ---- #

def number(f, i):
    global cpa, store
    #print("***Number", i, '"', f[i], '"')
    value = 0
    j = i+1
    while f[j].isdigit():
        j += 1
    value = int(f[i:j]) 
    #print("***Result =", value)
    return storeNumber (f, j, value)

# ---- octal ---- #

def octal(f, i):
    global cpa, store
    #print("****Octal", i, '"', f[i], '"')
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
        i += 1 # move to next digit
    if digits == 0:
        syntaxError(f, "no digits found after &")
    return storeNumber(f, i, value)

# ----binary ---- #

def binary(f, i):
    global cpa, store
    #print("***Binary", i, '"', f[i], '"')
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
            value = (value << 1) + 1
        elif digits == 0:
            syntaxError(f, "no digits found after B")
        else:
            return storeNumber(f, i, value)

# ---- store number ---- #

def storeNumber (f, i, value):
    global cpa, store
    double = True if f[i] == 'L' else False
    if double:
        i += 1
        if value > 2**35-1 or value < -2**35:
            syntaxError(f, "long number out of range")
        if cpa % 2 == 1:
            syntaxError(f, "Long number not aligned on an odd address")
        if ( (cpa+1) >= len(store)):
            syntaxError(f, "Store full")
        value = (value & 0o377777777777) << 1
        #print(format(value, "036b"))
        store[cpa]   = value &0o777777
        store[cpa+1] = value >> 18 
        #print(format(store[cpa], "018b"), format(store[cpa+1], "018b"), "\n\n")
        cpa += 2
    else: # short 
        if value > 2**17-1 or value < -2**17:
            syntaxError(f, "short number out of range")
        if cpa >= len(store):
            syntaxError(f, "Store full")
        value = (value & 0o377777) << 1
        store[cpa] = value
        cpa += 1
    return i

# ---- order ---- #

def order(f, i, p):
    global cpa, store, functions
    #print("***Order", i, '"', f[i], '"')
    order = functionCodes.find(f[i])
    if cpa >= len(store):
        syntaxError(f, "Store full")
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
    store[cpa] <<= 1
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
        if addr > 2047: # allow addresses to spill into spare bit
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
    elif f[i] == ';':
        return relative(f, i+1, p)
    else:
        #print("***Result =", 0)
        return i

# ---- relative ---- #

def relative(f, i, p):
    global cpa, store
    sign = f[i]
    value = 0
    if not (sign == '+' or  sign == '-'):
        syntaxError(f, "expected + or - after ;")
    i += 1
    if not f[i].isdigit:
        syntaxError(f, "number missing from relative address")
    while f[i].isdigit():
    	value = value * 10 + ord(f[i]) - ord('0')
    	i += 1
    addr = cpa + value * (+1 if sign == '+' else -1)
    if addr < 0 or addr > len(store):
        syntaxError(f, "relative address out of range 0", '-', len(store))
    store[cpa] += (addr << 1)
    return i

# ---- newline ---- #

def newline(f, i):
    global lineNo, lineStart
    #print("***Newline", lineNo, f[lineStart:i]);
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
    msg = "Error on line " + str(lineNo) + ": " + reason + '\n'
    lineEnd = f.index('\n', lineStart)
    msg = msg + f[lineStart:lineEnd]
    fail(msg)

 # ---- dumpStore, listStore ---- #

def dumpStore(f, list):
    #print("***Listing store")
    global cpa, store
    for i in range(len(store)):
        if list:
            f.write("%4d " % i)
        f.write(format(store[i], "018b"))
        if list:
            f.write("  ")
            value = store[i] >> 1
            fn = functionCodes[(value >> 12) & 31]
            ad = str((value >> 1) & 1023)
            lg = "D" if (value & 1 == 1) else "F"
            f.write("    " + fn + ad + lg)
        f.write('\n')

# ---- Error handling ---- #

def fail(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(1)

# ---- Decode arguments ---- #

def getArgs():
    global inFilePath, outFilePath, list, store
    parser = argparse.ArgumentParser(
            description='Simple EDSAC assembler for test programs')
    parser.add_argument('-list', action='store_true', help=
                        'produce annotated listing, otherwise just bit patterns')
    parser.add_argument('infile',  help='input file (or - for stdin)')
    parser.add_argument('-o', '--out', help='output file', default='-')
    parser.add_argument('-t', '--tanks', type =int, help='number of store tanks allowed',
                        default=1)
    args = parser.parse_args()
    inFilePath = args.infile
    outFilePath = args.out
    list = args.list
    if args.tanks< 1 or args.tanks > 32:
        print("Number of tanks must be in range 1..32");
        sys.exit(1)
    store = [ 0 for x in range(args.tanks*32)]

# ---- Main program ---- #

getArgs()
assembler()
