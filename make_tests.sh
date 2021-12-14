#!bin/sh
set -x
edsacasm tests/belltest.txt >tests/belltest.dat
edsacasm tests/xtest.txt >tests/xtest.dat
edsacasm tests/jmptest.txt >tests/jmptest.dat
edsacasm tests/countup.txt >tests/countup.dat
edsacasm tests/countdown.txt >tests/countdown.dat
edsacasm tests/addtest1.txt >tests/addtest1.dat
edsacasm tests/addtest2.txt >tests/addtest2.dat
edsacasm tests/addtest3.txt >tests/addtest3.dat
edsacasm tests/subtest1.txt >tests/subtest1.dat
edsacasm tests/subtest2.txt >tests/subtest2.dat
edsacasm tests/colltest1.txt >tests/colltest1.dat
edsacasm tests/colltest2.txt >tests/colltest2.dat
edsacasm tests/shifttest1.txt >tests/shifttest1.dat
edsacasm tests/shifttest2.txt >tests/shifttest2.dat
edsacasm tests/ytest.txt >tests/ytest.dat
edsacasm tests/tones.txt >tests/tones.dat




