#!/bin/bash
infile="$1"

time python2 algorithm.py $infile;
echo TIMING TEST DONE FOR PROPRIETARY ALGO >&2
time python2 NaiveTime.py $infile;
echo TIMING TEST DONE FOR NAIVE ALGO >&2
time python2 NormalTime.py $infile;
echo TIMING TEST DONE FOR NORMAL ALGO >&2
