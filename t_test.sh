#/bin/sh
set -x
edsacasm tests/$1.txt -list
edsacasm tests/$1.txt >tests/$1.dat
edsac -v2 -b tests/$1.dat -s




