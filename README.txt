Our Usage
1)Go to EECS584/input_files file and run command:
    python ../apriori.py -l input1.txt input2.txt input3.txt input4.txt input5.txt input6.txt -w 4 -s 0.1 -c 0.4
2)Go back to EECS584 head directory and run:
    ./run_tests.sh benchmarks/benchmark_name.txt > results_out.txt 
    (printing to output is to make it more readable)

Generic Usage:
-To create output file for apriori trained data
    python apriori.py -l INPUTFILE_1 INPUTFILE_2 ... -w WINDOW_SIZE(4) -s MIN_SUPPORT(0.1) -c MIN_CONFIDENCE(0.9)
-To generate a new random testcase run:
    python genRandQueries.py AllQueries.txt benchmark/benchmark_rand.txt
    (python genRandQueries.py <Input> <Output>)

File Locations: 
(Eg. file_in_git_repo -> path_to_spark_location)
-algorithm.py -> /spark-1.5.1/EECS584/algorithm.py
-AllQueries.txt -> /spark-1.5.1/EECS584/AllQueries.txt
-apriori.py -> /spark-1.5.1/EECS584/apriori.py
-benchmarks -> /spark-1.5.1/EECS584/benchmarks
-cacheBenchmark.py -> /spark-1.5.1/EECS584/cacheBenchmark.py
-GenRandStudentTable.py -> /spark-1.5.1/examples/src/main/resources/GenRandStudentTable.py
-input_files -> /spark-1.5.1/EECS584/input_files
-InputFile.txt -> /spark-1.5.1/EECS584/InputFile.txt
-NaiveTime.py -> /spark-1.5.1/EECS584/NaiveTime.py
-NormalTime.py -> /spark-1.5.1/EECS584/NormalTime.py
-run_tests.sh -> /spark-1.5.1/EECS584/run_tests.sh