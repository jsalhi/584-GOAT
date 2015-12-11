Our Usage
1)Put all our files submitted in the proper directory as listed in
    the file locations section of this README 
    (you will need to create the EECS584 directory)
2)Go to /spark-1.5.1/examples/src/main/resources/ and run the command
        python GenRandStudentTable.py
    In this script n is the number of tuples to be created in the 
    StudentTable, we tested with a dataset of 10 million tuples.
    Be warned creating a dataset of 10 million tuples will take around 
    5-10 minutes to run and will be around 3GB when complete.
3)Go to /spark-1.5.1/EECS584/ and edit algorithm.py. Change line 9 in
    this script to go to the proper path where you have stored the StudentTable
4)Go to /spark-1.5.1/EECS584/input_files file and run command:
        python ../apriori.py -l input1.txt input2.txt input3.txt input4.txt input5.txt input6.txt -w 4 -s 0.1 -c 0.4
    This command is responsible for creating the trained Apriori output
5)Go back to EECS584 head directory and run:
        ./run_tests.sh
    This command will run all of our benchmarks and can take anywhere from
    2 to 8 hours to complete, depending on machine.
    If you want to run just one test open up ./run_test.sh and you will
    see how to do that immediately, but each test itself will take from 
    6 minutes to an hour (again depending on machine)

Generic Usage:
-To create output file for apriori trained data
    python apriori.py -l INPUTFILE_1 INPUTFILE_2 ... -w WINDOW_SIZE(4) -s MIN_SUPPORT(0.1) -c MIN_CONFIDENCE(0.9)
-To generate a new random testcase run:
    python genRandQueries.py AllQueries.txt benchmark/benchmark_rand.txt
    (python genRandQueries.py <Input> <Output>)

-----------------------------------------------------------
Benchmarks:
h_h_h: Highly predictable workload, highly repetitive, high amount of columns
h_l_h: Highly predictable, low repeition, high amount of columns
l_h_h: Low prediction rate, high repetition, high amount of columns
l_l_h: Low prediction rate, low repetition, high amount of columns
h_h_l: Highly predictable workload, highly repetitive, low amount of columns
h_l_l: Highly predictable, low repeition, low amount of columns
l_h_l: Low prediction rate, high repetition, low amount of columns
l_l_l: Low prediction rate, low repetition, low amount of columns

-----------------------------------------------------------
File Locations: 
(Eg. file_in_git_repo -> path_to_spark_location)
-algorithm.py -> /spark-1.5.1/EECS584/algorithm.py
-AllQueries.txt -> /spark-1.5.1/EECS584/AllQueries.txt
-apriori.py -> /spark-1.5.1/EECS584/apriori.py
-benchmarks -> /spark-1.5.1/EECS584/benchmarks
-cacheBenchmark.py -> /spark-1.5.1/EECS584/cacheBenchmark.py
-GenRandStudentTable.py -> /spark-1.5.1/examples/src/main/resources/GenRandStudentTable.py
-genRandQueries.py -> /spark-1.5.1/EECS584/genRandQueries.py
-input_files -> /spark-1.5.1/EECS584/input_files
-NaiveTime.py -> /spark-1.5.1/EECS584/NaiveTime.py
-NormalTime.py -> /spark-1.5.1/EECS584/NormalTime.py
-run_tests.sh -> /spark-1.5.1/EECS584/run_tests.sh