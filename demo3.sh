#/bin/sh
set -x
edsacasm demos/demo3.txt -list
edsacasm demos/demo3.txt >demos/demo3.dat
edsac -v2 -b demos/demo3.dat -s | tprint
