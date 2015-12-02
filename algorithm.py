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
# key: simple query
# value: list of simple queries it associates with
apriori_simple_to_simple_map = {} # this will be populated by apriori script
# key: rdd pointer (is this possible?)
# value: set of columns that rdd can handle
# need to be sure to remove entry when RDD is evicted. 
rdd_to_rows_map = {} # this will be managed in code when new RDD is loaded
# key: simple query we wanted
# value: simple query that accounts for apriori associations
simple_to_simple_with_apriori_map = {} # this will be managed in preprocessing code

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
    apriori_simple_to_simple_map["SELECT GPA, Major FROM StudentTable"] = ["SELECT GPA, Major, Company FROM StudentTable"]
    rdd_to_rows_map['a'] = set(['GPA', 'Major', 'Company'])
    rdd_to_rows_map['b'] = set(['GPA', 'Major'])
    # preprocess the simple_to_simple_with_apriori_map
    for key, value in apriori_simple_to_simple_map.iteritems():
        print key
        print value
        built_query = build_query_for_rdd(key)
        simple_to_simple_with_apriori_map[key] = built_query
    print "pre-processed"
    print simple_to_simple_with_apriori_map

# Purpose: A proprietary framework to back propogate associated apriori
#           values to efficiently optimize a query workload using a 
#           distributed and cloud based platform. 
#           Implementation 1.0 ignores subdifferentials
# Input: nothing
# Returns: everything
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
            print "Line in input file was not valid/prepared for query: ", query
            sys.exit()
        # Check if there is already an RDD in memory that can address query
        columns_needed = extract_columns_from_query(simple_query)
        print columns_needed
        # iterate through RDDs in memory and see if any of them can support
        # the columns that are needed for this query
        rdd = "N/A"
        for key, value in rdd_to_rows_map.iteritems():
            # is columns needed a subset of the columns the RDD supports
            if columns_needed.issubset(value):
                rdd = key
                break
        print "RDD that can handle query: ", rdd
        # no RDD in memory can handle query, so we need to load in new one
        if rdd == "N/A":
            print "getting new rdd"
            rdd_query = simple_to_simple_with_apriori_map[simple_query]
            print rdd_query
            rdd = sqlContext.sql(rdd_query)
            rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
            # put new RDD in proper map

            # remove any evicted RDD's from proper map

        # do RDD ops needed
        if query not in complex_to_rdd_ops:
            print "Tried to get rdd_ops for invalid complex query: ", query
            sys.exit()
        rdd_ops = complex_to_rdd_ops[query]
        for op in rdd_ops:
            # do the op
            print "rdd_op"

# Purpose: extract all the columns needed for a certain query 
# Input: a simplified version of a query that contains only "SELECT cols FROM x"
# Returns: a set of all the columns that query is trying to access
def extract_columns_from_query(query):
    # remove commas that separate column names
    query = query.replace(",", "")
    words = query.split()
    columns = set()
    # 0 is SELECT
    for i in range(1,len(words)):
        if words[i] == "FROM":
            return columns
        columns.add(words[i])

# Purpose: Build a simple query that will be used to get an RDD
#           This query will account for any apriori associations found
# Input: a simplified version of a query that contains only "SELECT cols FROM x"
# Returns: the string query to run to get an RDD
def build_query_for_rdd(query):
    if query not in apriori_simple_to_simple_map:
        print "Tried to build a query from an invalid simple query: ", query
        sys.exit()
    associated_queries = apriori_simple_to_simple_map[query]
    columns_set = set()
    query_cols = extract_columns_from_query(query)
    for col in query_cols:
        columns_set.add(col)
    for item in associated_queries:
        query_cols = extract_columns_from_query(item)
        for col in query_cols:
            columns_set.add(col)
    # actually build query
    query_str = "SELECT "
    # add columns
    for column in columns_set:
        query_str = query_str + column + ", "
    # hacky way to remove last space a comma
    query_str = query_str[:-2]
    query_str = query_str + " FROM " + tableName
    return query_str

if __name__ == "__main__":
    pre_processing()
    proprietary_algo()








