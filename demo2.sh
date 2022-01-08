#/bin/sh
set -x
edsacasm demos/demo2.txt -list
edsacasm demos/demo2.txt >demos/demo2.dat
edsac -v2 -b demos/demo2.dat -s




