#!/bin/bash
infile="$1"

time python algorithm.py $infile
echo TIMING TEST DONE FOR PROPRIETARY ALGO >&2
time python NaiveTime.py $infile
echo TIMING TEST DONE FOR NAIVE ALGO >&2
time python NormalTime.py $infile
echo TIMING TEST DONE FOR NORMAL ALGO >&2