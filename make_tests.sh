#!bin/sh
set -x
edsacasm tests/belltest.txt >tests/belltest.dat
edsacasm tests/countup.txt >tests/countup.dat
edsacasm tests/countdown.txt >tests/countdown.dat
edsacasm tests/addtest1.txt >tests/addtest1.dat
edsacasm tests/addtest2.txt >tests/addtest2.dat
edsacasm tests/addtest3.txt >tests/addtest3.dat
edsacasm tests/subtest1.txt >tests/subtest1.dat


