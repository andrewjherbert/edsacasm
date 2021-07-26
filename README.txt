EDSAC TEST PROGRAM ASSEMBLER
============================

Andrew Herbert - 25/07/2021

The EDSAC TEST PROGRAM ASSEMBLER (edsacasm) is a simple assembler for writing short test
programs to be loaded into EDSAC store tank 0 using the Signal Sequence Injector (SSI).

It is an interim facility until such time as test programs can be loaded using EDSAC
initial orders.

esacasm is written in Python3 so that it can be readily run on any MacOS, Microsoft
Windows or Linux computer with a Python3 system installed.

COMMAND LINE
------------

python3 edsacasm.py [-h] [-list] [-infile INFILE] [-outfile OUTFILE]

-h          prints help on edsacasm command
-list       produce a listing as output
-infile     path to source program to assemble
-outfile    path to destination file for output

if -list is absent the output is a series of binary numbers, one per line for each of
the 64 words of tank 0, suitable for loading via the SSI, for example:

000000000000001011
000000000000001011
000000000000001011
010101000000010100
010011000000010101
010111000000001111
010000100000011100
001000000000011011
000100000000011000
000000000000010110
000000000000000000
000000000000000000
001101111000000000
010101011100000110
001001101010000111
010001001110011011
000000000000000000
000000000000000000
...
000000000000000000
000000000000000000

if -list is present the output is annotated with word number in decimal and a decode of
the content of that location as an EDSAC order, for example:

 0 000000000000001011    X0F
 1 000000000000001011    X0F
 2 000000000000001011    X0F
 3 010101000000010100    T10D
 4 010011000000010101    H12D
 5 010111000000001111    C14D
 6 010000100000011100    U16D
 7 001000000000011011    G1F
 8 000100000000011000    E2F
 9 000000000000010110    Z0F
10 000000000000000000    P0F
11 000000000000000000    P0F
12 001101111000000000    P123F
13 010101011100000110    S234D
14 001001101010000111    A345F
15 010001001110011011    G456D
16 000000000000000000    P0F
17 000000000000000000    P0F
...

This output format is intended to be useful for debugging and monitoring the execution of
the program during testing.

ASSEMBLY CODE
-------------

The assembler is rudimentary.  It allows the input of EDSAC orders and short numbers in a
form similar to that expected by the initial orders.  It also permits use of labels in
addition  to absolute addresses and the addition of comments.  It does not provide any of
the EDSAC initial orders facilities to support the use of library subroutines, floating
code etc.

The assembler is free format.  It reads a sequence of items where an item can be:


1) a comment consisting of a semicolon (;) followed by arbitrary text terminate by a
newline.

2) a short decimal number consisting of a + or - sign followed by a sequence of decimal
digits, e.g., +51, -633 etc.  Numbers must be in the range -65536 to +65535.

3) a short octal number consisting of an & symbol followed by a sequence of octal digits
(0-7). In addition the digit '8' can be used to insert a single 0 bit in the number and
the digit '9' can be used to insert a single 1.  This is a useful facility for
constructing words containing sub-fields.  For example, &7890 represents the binary number
11101000.

4) a short binary number consisting of the letter B followed by a sequence of binary
digits (1 and 0) e.g., B1011100011.

5) an order consisting of a single function letter (e.g., A, S, H, etc), and address and a
single length designator letter - F for short number operations, D for long number
operations.

The assembler recognises all the hardware defined operations plus P as a pseudo function
with code 0.  The  P code provides another way to enter numbers as is done in programs
intended to be loaded by initial orders.

An address can be either an absolute address expressed as a decimal integer in the range
0-63 or a reference to a label.  If the address field is omitted from an order, 0 is
assumed.

Labels consist or arbitrary text bracketed by full stops (.), as in .label. .1234. etc.

Any number of labels may be written before a comment, a number or an order.  The label
be assigned the address into which that number or order will be assembled.

When a label appears as an address in an order the address associated with the label
will be written to the order's address field.

Newline, space and tab characters can be used between items to improve layout.  Thus the
assembler allows multiple orders and numbers to written on a single line if desired.

The output shown earlier was produced by assembling the following input code:

; NIGEL 7

         XF             ; no op
.LOOP1.  XF
.LOOP2.  XF
         T .SCRAP. D
         H .OP1. D      ; load Multiplier
         C .OP2. D      ; Collate (AND)
         U .RESLT. D    ; store
         G .LOOP1. F    ; jump if >= 0
         E .LOOP2. F    ; jump if < 0
         ZF             ; stop and ring bell

.SCRAP.  +0
         +0
.OP1.    P123F
         S234D
.OP2.    A345F
         G456D
.RESLT.  +0
         +0

LOADING OUTPUT VIA SSI
----------------------

Instructions for loading code into the SSI are given in HN95 Signal Sequence Injector. The
basic mechanism is to connect a computer, e.g., a laptop to a USB port on the SSI unit,
connect to the SSI using minicom and then upload a file of binary numbers produce by the
assembler running with out the -list option.

Andrew Herbert 24 July 2021



