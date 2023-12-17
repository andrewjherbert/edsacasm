#/bin/sh
set -x
edsacasm tests/t$1.txt -list
edsacasm tests/t$1.txt >tests/t$1.dat
edsac -v2 -b tests/t$1.dat -s




