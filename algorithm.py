from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark import StorageLevel
import time
import sys

#Resource path + datafile
sparkResPath = "/home/jsalhi/spark-1.5.1/examples/src/main/resources/"
dataFile = sparkResPath + "StudentTable-1000.json"

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
rdd_to_cols_map = {} # this will be managed in code when new RDD is loaded
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
    complex_to_rdd_ops["SELECT AVG(GPA) FROM StudentTable WHERE Major = 'CSE'"] = [('Filter', 'Major', "==", 'CSE'), ('AVG', 'GPA')]
    complex_to_rdd_ops["SELECT AVG(GPA) FROM StudentTable WHERE Major = 'CS'"] = [('Filter', 'Major', "==", 'CS'), ('AVG', 'GPA')]
    apriori_simple_to_simple_map["SELECT GPA, Major FROM StudentTable"] = ["SELECT GPA, Major, Company FROM StudentTable"]
#    rdd_to_cols_map['a'] = set(['GPA', 'Major', 'Company'])
#    rdd_to_cols_map['b'] = set(['GPA', 'Major'])
    # preprocess the simple_to_simple_with_apriori_map
    for key, value in apriori_simple_to_simple_map.iteritems():
        built_query = build_query_for_rdd(key)
        simple_to_simple_with_apriori_map[key] = built_query
    print "pre-processed"

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
        # iterate through RDDs in memory and see if any of them can support
        # the columns that are needed for this query
        rdd = "N/A"
        for key, value in rdd_to_cols_map.iteritems():
            # is columns needed a subset of the columns the RDD supports
            # and is this RDD still in memory
            if columns_needed.issubset(value):
                print key
                storage_level = key.rdd.getStorageLevel()
                if storage_level == StorageLevel.MEMORY_ONLY:
                    print "found RDD in memory"
#                    rdd = key
#                    break
                else:
                    print "FOUND RDD THAT WAS EVICTED"
                rdd = key
                break
        # no RDD in memory can handle query, so we need to load in new one
        if rdd == "N/A":
            print "getting new rdd"
            rdd_query = simple_to_simple_with_apriori_map[simple_query]
            print rdd_query
            rdd = sqlContext.sql(rdd_query)
            rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
            # put new RDD in proper map
            rdd_to_cols_map[rdd] = extract_columns_from_query(rdd_query)
        # do RDD ops needed
        if query not in complex_to_rdd_ops:
            print "Tried to get rdd_ops for invalid complex query: ", query
            sys.exit()
        do_query_rdd_ops(rdd, query)

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
    print "There was no FROM in query: ", query
    return columns

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

# Purpose: Do RDD ops needed to answer the query that is given
# Input: the RDD we are operating on, and the complex query we are answering
# Returns: nothing
def do_query_rdd_ops(rdd, query):
    print "Doing RDD ops for query: ", query
    answer_rdd = rdd
    rdd_ops = complex_to_rdd_ops[query]
    for op in rdd_ops:
        # Find out what the op is and do it
        print "rdd_op"
        if op[0] == "Filter":
            print "Filter found"
            # op[1] = column
            # op[2] = filter styles: ==, <, <=, !=, >, >=
            # op[3] = value
            if op[2] == "==":
                answer_rdd = answer_rdd.filter(answer_rdd[op[1]] == op[3])
            elif op[2] == "!=":
                answer_rdd = answer_rdd.filter(answer_rdd[op[1]] != op[3])
            elif op[2] == "<":
                answer_rdd = answer_rdd.filter(answer_rdd[op[1]] < op[3])
            elif op[2] == "<=":
                answer_rdd = answer_rdd.filter(answer_rdd[op[1]] <= op[3])
            elif op[2] == ">":
                answer_rdd = answer_rdd.filter(answer_rdd[op[1]] > op[3])
            elif op[2] == ">=":
                answer_rdd = answer_rdd.filter(answer_rdd[op[1]] >= op[3])
#            print answer_rdd.take(10)
        elif op[0] == "AVG":
            print "AVG found"
            answer_rdd.groupBy().avg(op[1])
            print answer_rdd.groupBy().avg(op[1]).show()
        elif op[0] == "COUNT":
            print "COUNT found"
            answer_rdd.count()

if __name__ == "__main__":
    pre_processing()
    proprietary_algo()








