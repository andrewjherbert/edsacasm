#/bin/sh
set -x
edsacasm demos/demo1.txt -list
edsacasm demos/demo1.txt >demos/demo1.dat
edsac -v2 -b demos/demo1.dat -s




