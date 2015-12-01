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

complex_to_simple_map = {}
apriori_simple_to_simple_map = {}

# hard codes complex_to_simple_map
def pre_processing():
    complex_to_simple_map["SELECT AVG(GPA) FROM StudentTable WHERE Major = 'CSE'"] = "SELECT this"
    print "pre-processed"

def proprietary_algo():
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
            print "Line in input file was not valid/prepared for query"
            sys.exit()
        # Check if there is already an RDD in memory that can address query
        print line

if __name__ == "__main__":
    pre_processing()
    proprietary_algo()

# print "Starting Query A"
# query = "SELECT LastName FROM " + tableName + " WHERE FirstName = 'Alex'"
# rdd = sqlContext.sql(query)
# rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
# print "Starting Count A"
# rdd.count()







