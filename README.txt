TODO:
Alex:
-Write testing workload that we will evaluate performance on

Jaleel:
-Write ~5 files of example query workloads from a unique user
    Eg. User1 ran these 10 queries in this order, 
        User2 ran these 7 in this order, etc
-Write testing workload that we will evaluate performance on
-Tinker with apriori script and input files to see how 
    close you can get to what I'm looking for


Usage:
-To create output file for apriori trained data
    python apriori.py -l INPUTFILE_1 INPUTFILE_2 ... -w WINDOW_SIZE(4) -s MIN_SUPPORT(0.1) -c MIN_CONFIDENCE(0.9)

File Locations: 
(Eg. file_in_git_repo -> path_to_spark_location)
-algorithm.py -> /spark-1.5.1/EECS584/algorithm.py
-AllQueries.txt -> /spark-1.5.1/EECS584/AllQueries.txt
-apriori_out.txt -> /spark-1.5.1/EECS584/apriori_out.txt
-apriori.py -> /spark-1.5.1/EECS584/apriori.py
-cacheBenchmark.py -> /spark-1.5.1/EECS584/cacheBenchmark.py
-GenRandStudentTable.py -> /spark-1.5.1/examples/src/main/resources/GenRandStudentTable.py
-InputFile.txt -> /spark-1.5.1/EECS584/InputFile.txt
-NaiveTime.py -> /spark-1.5.1/EECS584/NaiveTime.py
-NormalTime.py -> /spark-1.5.1/EECS584/NormalTime.py
-input_files -> /spark-1.5.1/EECS584/input_files

Initial results on InputFile.txt and 10m dataset:
Algo: 6m 20s (380s)
Naive: 9m 45s (585s)
Normal: 9m 8s (548s)
Algo offered 35% speedup on naive and 31% on normal

apriori.py command on input files:
    python ../apriori.py -l input1.txt input2.txt input3.txt input4.txt input5.txt input6.txt -w 4 -s 0.1 -c 0.4