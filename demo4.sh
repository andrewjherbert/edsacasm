#/bin/sh
set -x
edsacasm demos/demo4.txt >demos/demo4.dat
edsac -v2 -b demos/demo4.dat -s | tprint





