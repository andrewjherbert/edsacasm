#/bin/sh
set -x
edsacasm tests/storetest.txt >tests/storetest.dat -t=32
edsac -b tests/storetest.dat -s | tprint