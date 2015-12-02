from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark import StorageLevel
import time
import sys

#Resource path + datafile
sparkResPath = "/Users/Alex/Desktop/spark-1.5.1/examples/src/main/resources/"
dataFile = sparkResPath + "StudentTable-10.json"

#Necessary garbage for setting up spark contexts
sc = SparkContext("local", "Cache Time Benchmark Evaluation")
sqlContext = SQLContext(sc)

#Read in data from datafile and register as temporary SQL table
tableName = "StudentTable"

print "Reading Table"
data = sqlContext.read.json(dataFile)
data.registerTempTable(tableName)

# key: complex query input (eg. "SELECT AVG(colx) FROM .... WHERE ...")
# value: simplified version of query (eg. "SELECT cols FROM ..." only)
complex_to_simple_map = {} # my understanding is this is going to be hard coded
# key: complex query input (eg. "SELECT AVG(colx) FROM .... WHERE ...")
# value: an ordered list of RDD ops that query needs 
#       ordering = list[0] done before list[1] and so on
complex_to_rdd_ops = {} # will this be hard coded? I think so

# hard codes complex_to_simple_map
# Purpose: do all preprocessing needed
#           1. hard code complex_to_simple map
#           2. pre load simple_to_simple_with_apriori_map
# Input: none
# Returns: nothing
def pre_processing():
    # next 7 hard coded lines are just to test to make sure algorithm works as should
    complex_to_simple_map["SELECT AVG(GPA) FROM StudentTable WHERE Major = 'CSE'"] = "SELECT GPA, Major FROM StudentTable"
    complex_to_simple_map["SELECT AVG(GPA) FROM StudentTable WHERE Major = 'CS'"] = "SELECT GPA, Major FROM StudentTable"
    complex_to_rdd_ops["SELECT AVG(GPA) FROM StudentTable WHERE Major = 'CSE'"] = [('filter', "Major = 'CSE'"), ('AVG', "GPA")]
    complex_to_rdd_ops["SELECT AVG(GPA) FROM StudentTable WHERE Major = 'CS'"] = [('filter', "Major = 'CS'"), ('AVG', "GPA")]
    print "pre-processed"

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
        if query in complex_to_simple_map:
            simple_query = complex_to_simple_map[query]
        else:
            print "Line in input file was not valid/prepared for query: ", query
            sys.exit()
        rdd = sqlContext.sql(simple_query)
        rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
        if query not in complex_to_rdd_ops:
            print "Tried to get rdd_ops for invalid complex query: ", query
            sys.exit()
        rdd_ops = complex_to_rdd_ops[query]
        for op in rdd_ops:
            # do the op
            print "rdd_op"

if __name__ == "__main__":
    pre_processing()
    NaiveAlgo()








