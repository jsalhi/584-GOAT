TODO:
Alex:
-Write backprop algorithm
-Evaluate benchmark metrics for JIT pipelining in TransMeta encoder setting

Jaleel:
-Write ~5 files of example query workloads from a unique user
    Eg. User1 ran these 10 queries in this order, 
        User2 ran these 7 in this order, etc
-Write testing workload that we will evaluate performance on

Usage:
-To create output file for apriori trained data
    python apriori.py -l INPUTFILE_1 INPUTFILE_2 ... -w WINDOW_SIZE(4) -s MIN_SUPPORT(0.2) -c MIN_CONFIDENCE(0.5)

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
