from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark import StorageLevel
import time
import sys
import algorithm as alg

# Take only the columns from each query, do filtering and RDD ops in RDD
def NaiveAlgo():
    if len(sys.argv) < 2:
        print "Not enough command line arguments"
        sys.exit()
    f = open(sys.argv[1])
    # Get all input queries in a list
    queries = f.readlines()
    queries = [line.strip('\n') for line in queries]
    for query in queries:
        # Get simplified version of query
        if query in alg.complex_to_simple_map:
            simple_query = alg.complex_to_simple_map[query]
        else:
            print "Line in input file was not valid/prepared for query: ", query
            sys.exit()
        rdd = alg.sqlContext.sql(simple_query)
        rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
        if query not in alg.complex_to_rdd_ops:
            print "Tried to get rdd_ops for invalid complex query: ", query
            sys.exit()
        alg.do_query_rdd_ops(rdd, query)

if __name__ == "__main__":
    alg.pre_processing()
    NaiveAlgo()








