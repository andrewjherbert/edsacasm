#!/bin/sh
set -x
python3 edsacasm.py tests/nigel2.txt >tests/nigel2.dat
python3 edsacasm.py tests/nigel3.txt >tests/nigel3.dat
python3 edsacasm.py tests/nigel7.txt >tests/nigel7.dat
python3 edsacasm.py tests/accutune1.txt >tests/accutune1.dat
python3 edsacasm.py tests/xtest.txt >tests/xtest.dat
python3 edsacasm.py tests/jmptest.txt >tests/jmptest.dat
python3 edsacasm.py tests/countup.txt >tests/countup.dat
python3 edsacasm.py tests/countdown.txt >tests/countdown.dat
python3 edsacasm.py tests/addtest1.txt >tests/addtest1.dat
python3 edsacasm.py tests/addtest2.txt >tests/addtest2.dat
python3 edsacasm.py tests/addtest3.txt >tests/addtest3.dat
python3 edsacasm.py tests/subtest1.txt >tests/subtest1.dat
python3 edsacasm.py tests/subtest2.txt >tests/subtest2.dat
python3 edsacasm.py tests/colltest1.txt >tests/colltest1.dat
python3 edsacasm.py tests/colltest2.txt >tests/colltest2.dat
python3 edsacasm.py tests/shifttest1.txt >tests/shifttest1.dat
python3 edsacasm.py tests/shifttest2.txt >tests/shifttest2.dat
python3 edsacasm.py tests/shifttest3.txt >tests/shifttest3.dat
python3 edsacasm.py tests/ytest.txt >tests/ytest.dat
python3 edsacasm.py tests/multtest1.txt >tests/multtest1.dat
python3 edsacasm.py tests/multtest2.txt >tests/multtest2.dat
python3 edsacasm.py tests/multtest3.txt >tests/multtest3.dat
python3 edsacasm.py tests/multtest4.txt >tests/multtest4.dat
python3 edsacasm.py tests/multtest5.txt >tests/multtest5.dat
python3 edsacasm.py tests/transftest.txt >tests/transftest.dat
python3 edsacasm.py tests/tutest.txt >tests/tutest.dat
python3 edsacasm.py tests/function-tests.txt >tests/function-tests.dat -t=32
python3 edsacasm.py tests/storetest.txt >tests/storetest.dat -t=32
python3 edsacasm.py tests/ztest.txt >tests/ztest.dat
python3 edsacasm.py tests/htest.txt >tests/htest.dat
python3 edsacasm.py tests/tsubroutine.txt >tests/tsubroutine.dat
python3 edsacasm.py tests/temp.txt >tests/temp.dat
python3 edsacasm.py tests/EZERO.txt >tests/EZERO.dat
python3 edsacasm.py tests/EPOS.txt >tests/EPOS.dat
python3 edsacasm.py tests/ENEG.txt >tests/ENEG.dat
python3 edsacasm.py tests/GZERO.txt >tests/GZERO.dat
python3 edsacasm.py tests/GPOS.txt >tests/GPOS.dat
python3 edsacasm.py tests/GNEG.txt >tests/GNEG.dat
