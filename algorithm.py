from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark import StorageLevel
from pprint import pprint
import time
import sys

#Resource path + datafile
sparkResPath = "/home/jsalhi/spark-1.5.1/examples/src/main/resources/"
#sparkResPath = "/Users/Alex/Desktop/spark-1.5.1/examples/src/main/resources/"
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
complex_to_simple_map = {} # hard coded
# key: complex query input (eg. "SELECT AVG(colx) FROM .... WHERE ...")
# value: an ordered list of RDD ops that query needs
#       ordering = list[0] done before list[1] and so on
complex_to_rdd_ops = {} # hard coded
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
    print "Starting pre-processing"
    init_hard_coded_complex_to_simple_map()
    init_hard_coded_complex_to_rdd_ops()
    # This will either be hard_coded or run the apriori script to do this
    init_apriori_simple_to_simple_map()
    # preprocess the simple_to_simple_with_apriori_map
    for key, value in apriori_simple_to_simple_map.iteritems():
        built_query = build_query_for_rdd(key)
        simple_to_simple_with_apriori_map[key] = built_query
    print "Finished pre-processing"

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
        _rdd = "N/A"
        for key, value in rdd_to_cols_map.iteritems():
            # is columns needed a subset of the columns the RDD supports
            # and is this RDD still in memory
            if columns_needed.issubset(value):
                storage_level = key.rdd.getStorageLevel()
                print "Storage level: ", storage_level
                # Currently not working but we want this to work
                if key.rdd.is_cached:
                    print "FOUND RDD IN MEMORY"
                    _rdd = key
                    break
                else:
                    print "FOUND RDD THAT WAS EVICTED"
        # no RDD in memory can handle query, so we need to load in new one
        if _rdd == "N/A":
            print "getting new rdd"
            rdd_query = simple_to_simple_with_apriori_map[simple_query]
            print "RDD query: ", rdd_query
            _rdd = sqlContext.sql(rdd_query)
            _rdd = _rdd.persist(StorageLevel.MEMORY_ONLY)
            # Make sure RDD is also persisting
            _rdd.rdd.persist(StorageLevel.MEMORY_ONLY)
            # put new RDD in proper map
            rdd_to_cols_map[_rdd] = extract_columns_from_query(rdd_query)

        # do RDD ops needed
        if query not in complex_to_rdd_ops:
            print "Tried to get rdd_ops for invalid complex query: ", query
            sys.exit()
        do_query_rdd_ops(_rdd, query)

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
        elif op[0] == "Group":
            print "Group by found"
            if op[1] == 'N/A':
                answer_rdd = answer_rdd.groupBy()
            else:
                if len(op) == 2:
                    answer_rdd = answer_rdd.groupBy(op[1])
                elif len(op) == 3:
                    answer_rdd = answer_rdd.groupBy(answer_rdd[op[1]], answer_rdd[op[2]])
        elif op[0] == "Select":
            print "Select found"
            if len(op) == 4:
                answer_rdd.select(answer_rdd[op[1]], answer_rdd[op[2]], answer_rdd[op[3]])
                print answer_rdd.select(answer_rdd[op[1]], answer_rdd[op[2]], answer_rdd[op[3]]).show()
            elif len(op) == 3:
                answer_rdd.select(answer_rdd[op[1]], answer_rdd[op[2]])
                print answer_rdd.select(answer_rdd[op[1]], answer_rdd[op[2]]).show()
            elif len(op) == 2:
                answer_rdd.select(answer_rdd[op[1]])
                print answer_rdd.select(answer_rdd[op[1]]).show()
        elif op[0] == "AVG":
            print "AVG found"
            answer_rdd.avg(op[1])
            print answer_rdd.avg(op[1]).show()
        elif op[0] == "MAX":
            print "MAX found"
            answer_rdd.max(op[1])
            print answer_rdd.max(op[1]).show()
        elif op[0] == "MIN":
            print "MIN found"
            answer_rdd.min(op[1])
            print answer_rdd.min(op[1]).show()
        elif op[0] == "COUNT":
            print "COUNT found"
            answer_rdd.count()
            print answer_rdd.count().show()

# Purpose: Initializes complex_to_simple_map with the hard coded info needed
# Input: nothing
# Returns: nothing
def init_hard_coded_complex_to_simple_map():
    print "Initializing complex_to_simple_map"
    complex_to_simple_map["SELECT AVG(GPA) FROM StudentTable GROUP BY Major"] = "SELECT GPA, Major FROM StudentTable"
    complex_to_simple_map["SELECT AVG(StartingSalary) FROM StudentTable WHERE Major = 'CSE'"] = "SELECT StartingSalary, Major FROM StudentTable"
    complex_to_simple_map["SELECT AVG(StartingSalary) FROM StudentTable WHERE Major = 'CSE' AND GPA > 3.5"] = "SELECT StartingSalary, Major, GPA FROM StudentTable"
    complex_to_simple_map["SELECT MAX(StartingSalary) FROM StudentTable WHERE Major = 'CSE'"] = "SELECT StartingSalary, Major FROM StudentTable"
    complex_to_simple_map["SELECT FirstName, LastName, Company FROM StudentTable WHERE Major = 'CSE' AND StartingSalary = 130000"] = "SELECT FirstName, LastName, Company, StartingSalary, Major FROM StudentTable"
    complex_to_simple_map["SELECT AVG(StartingSalary) FROM StudentTable GROUP BY BirthYear"] = "SELECT StartingSalary, BirthYear FROM StudentTable"
    complex_to_simple_map["SELECT AVG(StartingSalary) FROM StudentTable WHERE BirthYear = 1994 GROUP BY BirthMonth"] = "SELECT StartingSalary, BirthYear, BirthMonth FROM StudentTable"
    complex_to_simple_map["SELECT AVG(StartingSalary) FROM StudentTable WHERE BirthMonth = 'Mar' AND BirthYear = 1994 GROUP BY BirthDay"] = "SELECT StartingSalary, BirthYear, BirthMonth, BirthDay FROM StudentTable"
    complex_to_simple_map["SELECT AVG(GPA) FROM StudentTable GROUP BY BirthYear"] = "SELECT GPA, BirthYear FROM StudentTable"
    complex_to_simple_map["SELECT AVG(GPA) FROM StudentTable WHERE BirthYear = 1994 GROUP BY BirthMonth"] = "SELECT GPA, BirthYear, BirthMonth FROM StudentTable"
    complex_to_simple_map["SELECT AVG(GPA) FROM StudentTable WHERE BirthMonth = 'Mar' AND BirthYear = 1994 GROUP BY BirthDay"] = "SELECT GPA, BirthYear, BirthMonth, BirthDay FROM StudentTable"
    complex_to_simple_map["SELECT AVG(GPA) FROM StudentTable GROUP BY Gender"] = "SELECT GPA, Gender FROM StudentTable"
    complex_to_simple_map["SELECT AVG(StartingSalary) FROM StudentTable GROUP BY Gender"] = "SELECT StartingSalary, Gender FROM StudentTable"
    complex_to_simple_map["SELECT COUNT(StudentID) FROM StudentTable GROUP BY Gender, Major"] = "SELECT StudentID, Major, Gender FROM StudentTable"
    complex_to_simple_map["SELECT AVG(StartingSalary) FROM StudentTable GROUP BY Company"] = "SELECT StartingSalary, Company FROM StudentTable"
    complex_to_simple_map["SELECT AVG(GPA) FROM StudentTable GROUP BY Company"] = "SELECT GPA, Company FROM StudentTable"
    complex_to_simple_map["SELECT MIN(GPA) FROM StudentTable WHERE Company = 'Google'"] = "SELECT GPA, Company FROM StudentTable"
    complex_to_simple_map["SELECT COUNT(StudentID) FROM StudentTable GROUP BY Company, Major"] = "SELECT StudentID, Company, Major FROM StudentTable"
    complex_to_simple_map["SELECT COUNT(StudentID) FROM StudentTable GROUP BY Company, TuitionType"] = "SELECT StudentID, Company, TuitionType FROM StudentTable"
    complex_to_simple_map["SELECT MAX(StartingSalary) FROM StudentTable GROUP BY Company"] = "SELECT StartingSalary, Company FROM StudentTable"
    complex_to_simple_map["SELECT MAX(StartingSalary) FROM StudentTable GROUP BY Major"] = "SELECT StartingSalary, Major FROM StudentTable"
    complex_to_simple_map["SELECT MAX(StartingSalary) FROM StudentTable GROUP BY TuitionType"] = "SELECT StartingSalary, TuitionType FROM StudentTable"
    complex_to_simple_map["SELECT MIN(StartingSalary) FROM StudentTable GROUP BY Company"] = "SELECT StartingSalary, Company FROM StudentTable"
    complex_to_simple_map["SELECT MIN(StartingSalary) FROM StudentTable GROUP BY Major"] = "SELECT StartingSalary, Major FROM StudentTable"
    complex_to_simple_map["SELECT MIN(StartingSalary) FROM StudentTable GROUP BY TuitionType"] = "SELECT StartingSalary, TuitionType FROM StudentTable"
    complex_to_simple_map["SELECT COUNT(StudentID) FROM StudentTable GROUP BY FavoriteClass"] = "SELECT StudentID, FavoriteClass FROM StudentTable"
    complex_to_simple_map["SELECT AVG(StartingSalary) FROM StudentTable WHERE FavoriteClass = 'EECS584'"] = "SELECT StartingSalary, FavoriteClass FROM StudentTable"
    complex_to_simple_map["SELECT FirstName, LastName FROM StudentTable WHERE FavoriteClass = 'EECS584'"] = "SELECT FirstName, LastName, FavoriteClass FROM StudentTable"
    complex_to_simple_map["SELECT AVG(BirthYear) FROM StudentTable GROUP BY Year"] = "SELECT BirthYear, Year FROM StudentTable"
    complex_to_simple_map["SELECT AVG(RandInt) FROM StudentTable GROUP BY Year"] = "SELECT RandInt, Year FROM StudentTable"
    print "Finished initializing complex_to_simple_map"

# Purpose: Initializes complex_to_rdd_ops with the hard coded info needed
# Input: nothing
# Returns: nothing
def init_hard_coded_complex_to_rdd_ops():
    print "Initializing complex_to_rdd_ops"
    # Every entry must have a tuple that is ('Group', col_name)
    # If there is no group by make that tuple ('Group', 'N/A')
    # EXCEPTION: If it is only SELECT cols with no RDD op then no ('Group', ...) tuple
    complex_to_rdd_ops["SELECT AVG(GPA) FROM StudentTable GROUP BY Major"] = [('Group', 'Major'), ('AVG', 'GPA')]
    complex_to_rdd_ops["SELECT AVG(StartingSalary) FROM StudentTable WHERE Major = 'CSE'"] = [('Filter', 'Major', "==", 'CSE'), ('Group', 'N/A'), ('AVG', 'StartingSalary')]
    complex_to_rdd_ops["SELECT AVG(StartingSalary) FROM StudentTable WHERE Major = 'CSE' AND GPA > 3.5"] = [('Filter', 'Major', "==", 'CSE'), ('Filter', 'GPA', ">", 3.5), ('Group', 'N/A'), ('AVG', 'StartingSalary')]
    complex_to_rdd_ops["SELECT MAX(StartingSalary) FROM StudentTable WHERE Major = 'CSE'"] = [('Filter', 'Major', "==", 'CSE'), ('Group', 'N/A'), ('MAX', 'StartingSalary')]
    complex_to_rdd_ops["SELECT FirstName, LastName, Company FROM StudentTable WHERE Major = 'CSE' AND StartingSalary = 130000"] = [('Filter', 'Major', "==", 'CSE'), ('Filter', 'StartingSalary', "==", 130000), ('Select', 'FirstName', 'LastName', 'Company')]
    complex_to_rdd_ops["SELECT AVG(StartingSalary) FROM StudentTable GROUP BY BirthYear"] = [('Group', 'BirthYear'), ('AVG', 'StartingSalary')]
    complex_to_rdd_ops["SELECT AVG(StartingSalary) FROM StudentTable WHERE BirthYear = 1994 GROUP BY BirthMonth"] = [('Filter', 'BirthYear', "==", 1994), ('Group', 'BirthMonth'), ('AVG', 'StartingSalary')]
    complex_to_rdd_ops["SELECT AVG(StartingSalary) FROM StudentTable WHERE BirthMonth = 'Mar' AND BirthYear = 1994 GROUP BY BirthDay"] = [('Filter', 'BirthYear', "==", 1994), ('Filter', 'BirthMonth', "==", 'Mar'), ('Group', 'BirthDay'), ('AVG', 'StartingSalary')]
    complex_to_rdd_ops["SELECT AVG(GPA) FROM StudentTable GROUP BY BirthYear"] = [('Group', 'BirthYear'), ('AVG', 'GPA')]
    complex_to_rdd_ops["SELECT AVG(GPA) FROM StudentTable WHERE BirthYear = 1994 GROUP BY BirthMonth"] = [('Filter', 'BirthYear', "==", 1994), ('Group', 'BirthMonth'), ('AVG', 'GPA')]
    complex_to_rdd_ops["SELECT AVG(GPA) FROM StudentTable WHERE BirthMonth = 'Mar' AND BirthYear = 1994 GROUP BY BirthDay"] = [('Filter', 'BirthYear', "==", 1994), ('Filter', 'BirthMonth', "==", 'Mar'), ('Group', 'BirthDay'), ('AVG', 'GPA')]
    complex_to_rdd_ops["SELECT AVG(GPA) FROM StudentTable GROUP BY Gender"] = [('Group', 'Gender'), ('AVG', 'GPA')]
    complex_to_rdd_ops["SELECT AVG(StartingSalary) FROM StudentTable GROUP BY Gender"] = [('Group', 'Gender'), ('AVG', 'StartingSalary')]
    complex_to_rdd_ops["SELECT COUNT(StudentID) FROM StudentTable GROUP BY Gender, Major"] = [('Group', 'Gender', 'Major'), ('COUNT', 'StudentID')]
    complex_to_rdd_ops["SELECT AVG(StartingSalary) FROM StudentTable GROUP BY Company"] = [('Group', 'Company'), ('AVG', 'StartingSalary')]
    complex_to_rdd_ops["SELECT AVG(GPA) FROM StudentTable GROUP BY Company"] = [('Group', 'Company'), ('AVG', 'GPA')]
    complex_to_rdd_ops["SELECT MIN(GPA) FROM StudentTable WHERE Company = 'Google'"] = [('Filter', 'Company', "==", 'Google'), ('Group', 'N/A'), ('MIN', 'GPA')]
    complex_to_rdd_ops["SELECT COUNT(StudentID) FROM StudentTable GROUP BY Company, Major"] = [('Group', 'Company', 'Major'), ('COUNT', 'StudentID')]
    complex_to_rdd_ops["SELECT COUNT(StudentID) FROM StudentTable GROUP BY Company, TuitionType"] = [('Group', 'Company', 'TuitionType'), ('COUNT', 'StudentID')]
    complex_to_rdd_ops["SELECT MAX(StartingSalary) FROM StudentTable GROUP BY Company"] = [('Group', 'Company'), ('MAX', 'StartingSalary')]
    complex_to_rdd_ops["SELECT MAX(StartingSalary) FROM StudentTable GROUP BY Major"] = [('Group', 'Major'), ('MAX', 'StartingSalary')]
    complex_to_rdd_ops["SELECT MAX(StartingSalary) FROM StudentTable GROUP BY TuitionType"] = [('Group', 'TuitionType'), ('MAX', 'StartingSalary')]
    complex_to_rdd_ops["SELECT MIN(StartingSalary) FROM StudentTable GROUP BY Company"] = [('Group', 'Company'), ('MIN', 'StartingSalary')]
    complex_to_rdd_ops["SELECT MIN(StartingSalary) FROM StudentTable GROUP BY Major"] = [('Group', 'Major'), ('MIN', 'StartingSalary')]
    complex_to_rdd_ops["SELECT MIN(StartingSalary) FROM StudentTable GROUP BY TuitionType"] = [('Group', 'TuitionType'), ('MIN', 'StartingSalary')]
    complex_to_rdd_ops["SELECT COUNT(StudentID) FROM StudentTable GROUP BY FavoriteClass"] = [('Group', 'FavoriteClass'), ('COUNT', 'StudentID')]
    complex_to_rdd_ops["SELECT AVG(StartingSalary) FROM StudentTable WHERE FavoriteClass = 'EECS584'"] = [('Filter', 'FavoriteClass', "==", 'EECS584'), ('Group', 'N/A'), ('AVG', 'StartingSalary')]
    complex_to_rdd_ops["SELECT FirstName, LastName FROM StudentTable WHERE FavoriteClass = 'EECS584'"] = [('Filter', 'FavoriteClass', "==", 'EECS584'), ('Select', 'FirstName', 'LastName')]
    complex_to_rdd_ops["SELECT AVG(BirthYear) FROM StudentTable GROUP BY Year"] = [('Group', 'Year'), ('AVG', 'BirthYear')]
    complex_to_rdd_ops["SELECT AVG(RandInt) FROM StudentTable GROUP BY Year"] = [('Group', 'Year'), ('AVG', 'RandInt')]
    print "Finished initializing complex_to_rdd_ops"

def init_apriori_simple_to_simple_map():
    print "Initializing apriori_simple_to_simple_map"
    # These should be populated by apriori part, not hard coded
    # And it should be a list of queries, not just one (for most cases)
    apriori_simple_to_simple_map["SELECT GPA, Major FROM StudentTable"] = ["SELECT GPA, Major FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StartingSalary, Major, GPA FROM StudentTable"] = ["SELECT StartingSalary, Major, GPA FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StartingSalary, Major FROM StudentTable"] = ["SELECT StartingSalary, Major FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT FirstName, LastName, Company, StartingSalary, Major FROM StudentTable"] = ["SELECT FirstName, LastName, Company, StartingSalary, Major FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StartingSalary, BirthYear FROM StudentTable"] = ["SELECT StartingSalary, BirthYear FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StartingSalary, BirthYear, BirthMonth FROM StudentTable"] = ["SELECT StartingSalary, BirthYear, BirthMonth FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StartingSalary, BirthYear, BirthMonth, BirthDay FROM StudentTable"] = ["SELECT StartingSalary, BirthYear, BirthMonth, BirthDay FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT GPA, BirthYear FROM StudentTable"] = ["SELECT GPA, BirthYear FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT GPA, BirthYear, BirthMonth FROM StudentTable"] = ["SELECT GPA, BirthYear, BirthMonth FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT GPA, BirthYear, BirthMonth, BirthDay FROM StudentTable"] = ["SELECT GPA, BirthYear, BirthMonth, BirthDay FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT GPA, Gender FROM StudentTable"] = ["SELECT GPA, Gender FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StartingSalary, Gender FROM StudentTable"] = ["SELECT StartingSalary, Gender FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StudentID, Major, Gender FROM StudentTable"] = ["SELECT StudentID, Major, Gender FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StartingSalary, Company FROM StudentTable"] = ["SELECT StartingSalary, Company FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT GPA, Company FROM StudentTable"] = ["SELECT GPA, Company FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StudentID, Company, Major FROM StudentTable"] = ["SELECT StudentID, Company, Major FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StudentID, Company, TuitionType FROM StudentTable"] = ["SELECT StudentID, Company, TuitionType FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StartingSalary, Major FROM StudentTable"] = ["SELECT StartingSalary, Major FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StartingSalary, TuitionType FROM StudentTable"] = ["SELECT StartingSalary, TuitionType FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StudentID, FavoriteClass FROM StudentTable"] = ["SELECT StudentID, FavoriteClass FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT StartingSalary, FavoriteClass FROM StudentTable"] = ["SELECT StartingSalary, FavoriteClass FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT FirstName, LastName, FavoriteClass FROM StudentTable"] = ["SELECT FirstName, LastName, FavoriteClass FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT BirthYear, Year FROM StudentTable"] = ["SELECT BirthYear, Year FROM StudentTable"]
    apriori_simple_to_simple_map["SELECT RandInt, Year FROM StudentTable"] = ["SELECT RandInt, Year FROM StudentTable"]
    file_opened = True
    try:
        apriori_in = open("apriori_out.txt")
    except IOError:
        file_opened = False
        print "Could not open apriori file"
    if file_opened:
        print "Apriori File Opened"
        associations = apriori_in.readlines()
        associations = [line.strip('\n') for line in associations]
        for i in range(0,len(associations)):
            if associations[i].isdigit():
                key = complex_to_simple_map[associations[i+1]]
                # Remove older entry
                apriori_simple_to_simple_map[key] = []
                for j in range(1, int(associations[i])+1):
                    value = complex_to_simple_map[associations[i+j]]
                    apriori_simple_to_simple_map[key].append(value)
    print "Finished initializing apriori_simple_to_simple_map"

if __name__ == "__main__":
    pre_processing()
    proprietary_algo()








