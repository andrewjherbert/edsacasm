#/bin/sh
set -x
edsacasm tests/function-tests.txt >function-tests.dat -t=32
edsac -v -b tests/function-tests.dat -s