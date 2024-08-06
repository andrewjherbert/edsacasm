#/bin/sh
set -x
python3 edsacasm tests/$1.txt -list $2
python3 edsacasm tests/$1.txt >tests/$1.dat $2
edsac -v2 -b tests/$1.dat -s




