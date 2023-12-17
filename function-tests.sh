#/bin/sh
set -x
edsacasm tests/function-tests.txt >function-tests.dat -t=32
edsac -v1 -b tests/function-tests.dat -s