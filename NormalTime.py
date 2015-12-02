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
# value: simplified version of query (eg. "SELECT cols FROM ... WHERE ..." only)
complex_to_simpler_map = {} # my understanding is this is going to be hard coded
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
    complex_to_simpler_map["SELECT AVG(GPA) FROM StudentTable WHERE Major = 'CSE'"] = "SELECT GPA FROM StudentTable WHERE Major = 'CSE'"
    complex_to_simpler_map["SELECT AVG(GPA) FROM StudentTable WHERE Major = 'CS'"] = "SELECT GPA FROM StudentTable WHERE Major = 'CS'"
    complex_to_rdd_ops["SELECT AVG(GPA) FROM StudentTable WHERE Major = 'CSE'"] = [('AVG', "GPA")]
    complex_to_rdd_ops["SELECT AVG(GPA) FROM StudentTable WHERE Major = 'CS'"] = [('AVG', "GPA")]

# Take the query as is, leave the where clause in, only separate out the RDD ops
def NormalTime():
    if len(sys.argv) < 2:
        print "Not enough command line arguments"
        sys.exit()
    f = open(sys.argv[1])
    # Get all input queries in a list
    queries = f.readlines()
    queries = [line.strip('\n') for line in queries]
    for query in queries:
        # Get simplified version of query
        if query in complex_to_simpler_map:
            simpler_query = complex_to_simpler_map[query]
        else:
            print "Line in input file was not valid/prepared for query: ", query
            sys.exit()
        rdd = sqlContext.sql(simpler_query)
        rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
        # do RDD ops needed
        if query not in complex_to_rdd_ops:
            print "Tried to get rdd_ops for invalid complex query: ", query
            sys.exit()
        rdd_ops = complex_to_rdd_ops[query]
        for op in rdd_ops:
            # do the op
            print "rdd_op"

if __name__ == "__main__":
    pre_processing()
    NormalTime()








