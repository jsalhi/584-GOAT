#!/bin/bash
infile="$1"

time python algorithm.py $infile
echo "TIMING TEST DONE FOR PROPRIETARY ALGO"
time python NaiveTime.py $infile
echo "TIMING TEST DONE FOR NAIVE ALGO"
time python NormalTime.py $infile
echo "TIMING TEST DONE FOR NORMAL ALGO"