TODO:
Alex:
-Test if groupby with RDD works 
-Write a set of all potential queries (around 20 or 30)
-Write ~5 files of example query workloads from a unique user
    Eg. User1 ran these 5 queries in this order, 
        User2 ran these 7 in this order, etc
-Add something to handle if RDD is in memory or not
-Hard code everything that is needed for queries

Jaleel:
-Write a function that takes in a list of files of queries 
and trains apriori on that


File Locations: 
(Eg. file_in_git_repo -> path_to_spark_location)
-algorithm.py -> /spark-1.5.1/EECS584/algorithm.py
-apriori.py -> ???????
-cacheBenchmark.py -> /spark-1.5.1/EECS584/cacheBenchmark.py
-GenRandStudentTable.py -> /spark-1.5.1/examples/src/main/resources/GenRandStudentTable.py
-InputFile.txt -> /spark-1.5.1/EECS584/InputFile.txt
-NaiveTime.py -> /spark-1.5.1/EECS584/NaiveTime.py
-NormalTime.py -> /spark-1.5.1/EECS584/NormalTime.py