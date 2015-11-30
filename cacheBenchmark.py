from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark import StorageLevel
import time

##############
#GLOBALS INIT
##############

#Number of iterations to compute avg exec time
#
nFuncIters = 100

#Resource path + datafile
#
sparkResPath = "/Users/Alex/Desktop/spark-1.5.1/examples/src/main/resources/"
dataFile = sparkResPath + "StudentTable-10000000.json"

#Necessary garbage for setting up spark contexts
#
sc = SparkContext("local", "Cache Time Benchmark Evaluation")
sqlContext = SQLContext(sc)

#Read in data from datafile and register as temporary SQL table
#
tableName = "RandDataTable"

print "Reading Table"
data = sqlContext.read.json(dataFile)
data.registerTempTable(tableName)

print "Starting Query A"
print "Starting Time"
start_time = time.time()
query = "SELECT LastName FROM " + tableName + " WHERE FirstName = 'Alex'"
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
print "Starting Count A"
rdd.count()
print "Starting Query B"
query = "SELECT FirstName FROM " + tableName + " WHERE LastName = 'Lancaster'"
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
print "Starting Count B"
rdd.count()
print "Starting Query C"
query = "SELECT Company FROM " + tableName + " WHERE StartingSalary = 130000"
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
print "Starting Count C"
rdd.count()
end_time = time.time()
print "A then B Time took:", end_time-start_time

print "Starting Query A"
print "Starting Time"
start_time = time.time()
query = "SELECT LastName, FirstName FROM " + tableName
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
rdd2 = rdd.filter(rdd['FirstName'] == 'Alex')
print "Starting Count A"
rdd2.count()
print "Starting Query B"
query = "SELECT FirstName, LastName FROM " + tableName
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
rdd2 = rdd.filter(rdd['LastName'] == 'Lancaster')
print "Starting Count B"
rdd2.count()
print "Starting Query C"
query = "SELECT Company, StartingSalary FROM " + tableName
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
rdd2 = rdd.filter(rdd['StartingSalary'] == 130000)
print "Starting Count C"
rdd2.count()
end_time = time.time()
print "A then B Time took:", end_time-start_time

print "Starting Query A&B"
print "Starting Time"
start_time = time.time()
query = "SELECT FirstName, LastName, Company, StartingSalary FROM " + tableName
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
print "Starting Filter A"
rdd2 = rdd.filter(rdd['FirstName'] == 'Alex')
print "Starting Count A"
rdd2.count()
print "Starting Filter B"
rdd3 = rdd.filter(rdd['LastName'] == 'Lancaster')
print "Starting Count B"
rdd3.count()
print "Starting Filter C"
rdd4 = rdd.filter(rdd['StartingSalary'] == 130000)
print "Starting Count C"
rdd4.count()
end_time = time.time()
print "A and B Time took:", end_time-start_time

# print "Starting Query A"
# print "Starting Time"
# start_time = time.time()
# query = "SELECT RandInt FROM " + tableName + " WHERE RandInt = 3"
# rdd = sqlContext.sql(query)
# rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
# print "Starting Count A"
# rdd.count()
# print "Starting Query B"
# query = "SELECT RandString FROM " + tableName + " WHERE RandString = 'aaa'"
# rdd = sqlContext.sql(query)
# rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
# print "Starting Count B"
# rdd.count()
# print "Starting Query C"
# query = "SELECT RandString FROM " + tableName + " WHERE RandString = 'bbb'"
# rdd = sqlContext.sql(query)
# rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
# print "Starting Count C"
# rdd.count()
# end_time = time.time()
# print "A then B Time took:", end_time-start_time

# print "Starting Query A"
# print "Starting Time"
# start_time = time.time()
# query = "SELECT RandInt FROM " + tableName
# rdd = sqlContext.sql(query)
# rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
# rdd2 = rdd.filter(rdd['RandInt'] == 3)
# print "Starting Count A"
# rdd2.count()
# print "Starting Query B"
# query = "SELECT RandString FROM " + tableName
# rdd = sqlContext.sql(query)
# rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
# rdd2 = rdd.filter(rdd['RandString'] == 'aaa')
# print "Starting Count B"
# rdd2.count()
# print "Starting Query C"
# query = "SELECT RandString FROM " + tableName
# rdd = sqlContext.sql(query)
# rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
# rdd2 = rdd.filter(rdd['RandString'] == 'bbb')
# print "Starting Count C"
# rdd2.count()
# end_time = time.time()
# print "A then B Time took:", end_time-start_time

# print "Starting Query A&B"
# print "Starting Time"
# start_time = time.time()
# query = "SELECT RandInt, RandString FROM " + tableName
# rdd = sqlContext.sql(query)
# rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
# print "Starting Filter A"
# rdd2 = rdd.filter(rdd['RandInt'] == 3)
# print "Starting Count A"
# rdd2.count()
# print "Starting Filter B"
# rdd3 = rdd.filter(rdd['RandString'] == 'aaa')
# print "Starting Count B"
# rdd3.count()
# print "Starting Filter C"
# rdd4 = rdd.filter(rdd['RandString'] == 'bbb')
# print "Starting Count C"
# rdd4.count()
# end_time = time.time()
# print "A and B Time took:", end_time-start_time



