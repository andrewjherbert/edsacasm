#!/bin/sh
set -x
edsacasm tests/nigel2.txt >tests/nigel2.dat
edsacasm tests/nigel3.txt >tests/nigel3.dat
edsacasm tests/nigel7.txt >tests/nigel7.dat
edsacasm tests/accutune1.txt >tests/accutune1.dat
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
edsacasm tests/shifttest3.txt >tests/shifttest3.dat
edsacasm tests/ytest.txt >tests/ytest.dat
edsacasm tests/multtest1.txt >tests/multtest1.dat
edsacasm tests/multtest2.txt >tests/multtest2.dat
edsacasm tests/multtest3.txt >tests/multtest3.dat
edsacasm tests/multtest4.txt >tests/multtest4.dat
edsacasm tests/multtest5.txt >tests/multtest5.dat
edsacasm tests/transftest.txt >tests/transftest.dat
edsacasm tests/tutest.txt >tests/tutest.dat
edsacasm tests/function-tests.txt >tests/function-tests.dat -t=32
edsacasm tests/storetest.txt >tests/storetest.dat -t=32
edsacasm tests/hloop.txt >tests/hloop.dat
edsacasm tests/ztest.txt >tests/ztest.dat




