from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark import StorageLevel
import time
import sys
import algorithm as alg

# Take the query as is, how long does the SQL itself take if not at all optimized by RDD
def NormalTime():
    if len(sys.argv) < 2:
        print "Not enough command line arguments"
        sys.exit()
    f = open(sys.argv[1])
    # Get all input queries in a list
    queries = f.readlines()
    queries = [line.strip('\n') for line in queries]
    for query in queries:
        rdd = alg.sqlContext.sql(query)
        rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
        rdd.show()

if __name__ == "__main__":
    alg.pre_processing()
    NormalTime()








