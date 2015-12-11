#!/bin/bash

echo "RUNNING H_H_H"
./run_one_test.sh benchmarks/h_h_h.txt > results/h_h_h_out.txt.verbose
echo "FINISHD H_H_H"

echo "RUNNING H_H_L"
./run_one_test.sh benchmarks/h_h_l.txt > results/h_h_l_out.txt.verbose
echo "FINISHD H_H_L"

echo "RUNNING H_L_L"
./run_one_test.sh benchmarks/h_l_l.txt > results/h_l_l_out.txt.verbose
echo "FINISHD H_L_L"

echo "RUNNING H_L_H"
./run_one_test.sh benchmarks/h_l_h.txt > results/h_l_h_out.txt.verbose
echo "FINISHD H_L_H"

echo "RUNNING L_L_L"
./run_one_test.sh benchmarks/l_l_l.txt > results/l_l_l_out.txt.verbose
echo "FINISHD L_L_L"

echo "RUNNING L_L_H"
./run_one_test.sh benchmarks/l_l_h.txt > results/l_l_h_out.txt.verbose
echo "FINISHD L_L_H"

echo "RUNNING L_H_H"
./run_one_test.sh benchmarks/l_h_h.txt > results/l_h_h_out.txt.verbose
echo "FINISHD L_H_H"

echo "RUNNING L_H_L"
./run_one_test.sh benchmarks/l_h_l.txt > results/l_h_l_out.txt.verbose
echo "FINISHD L_H_L"

echo "RUNNING RAND"
./run_one_test.sh benchmarks/rand.txt > results/rand_out.txt.verbose
echo "FINISHD RAND"
