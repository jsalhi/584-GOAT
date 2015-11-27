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
dataFile = sparkResPath + "repeatedDataset-10000000.json"

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
query = "SELECT RandInt FROM " + tableName + " WHERE RandInt = 3"
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
print "Starting Count A"
rdd.count()
print "Starting Query B"
query = "SELECT RandString FROM " + tableName + " WHERE RandString = 'aaa'"
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
print "Starting Count B"
rdd.count()
print "Starting Query C"
query = "SELECT RandString FROM " + tableName + " WHERE RandString = 'bbb'"
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
print "Starting Count C"
rdd.count()
end_time = time.time()
print "A then B Time took:", end_time-start_time

print "Starting Query A"
print "Starting Time"
start_time = time.time()
query = "SELECT RandInt FROM " + tableName
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
rdd2 = rdd.filter(rdd['RandInt'] == 3)
print "Starting Count A"
rdd2.count()
print "Starting Query B"
query = "SELECT RandString FROM " + tableName
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
rdd2 = rdd.filter(rdd['RandString'] == 'aaa')
print "Starting Count B"
rdd2.count()
print "Starting Query C"
query = "SELECT RandString FROM " + tableName
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
rdd2 = rdd.filter(rdd['RandString'] == 'bbb')
print "Starting Count C"
rdd2.count()
end_time = time.time()
print "A then B Time took:", end_time-start_time

print "Starting Query A&B"
print "Starting Time"
start_time = time.time()
query = "SELECT RandInt, RandString FROM " + tableName
rdd = sqlContext.sql(query)
rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
print "Starting Filter A"
rdd2 = rdd.filter(rdd['RandInt'] == 3)
print "Starting Count A"
rdd2.count()
print "Starting Filter B"
rdd3 = rdd.filter(rdd['RandString'] == 'aaa')
print "Starting Count B"
rdd3.count()
print "Starting Filter C"
rdd4 = rdd.filter(rdd['RandString'] == 'bbb')
print "Starting Count C"
rdd4.count()
end_time = time.time()
print "A and B Time took:", end_time-start_time

# print "Starting Query"
# query = "SELECT * FROM " + tableName + " WHERE RandString = 'aaa'"
# rdd = sqlContext.sql(query)
# print "Starting Count"
# start_time = time.time()
# rdd = rdd.persist(StorageLevel.MEMORY_ONLY)
# rdd.count()
# end_time = time.time()
# print "Time took:", end_time-start_time

# query2 = "SELECT * FROM " + tableName + " WHERE RandString = 'bbb'"
# rdd2 = sqlContext.sql(query2)
# print "Starting Count2"
# start_time = time.time()
# rdd2.count()
# end_time = time.time()
# print "Time 2 took:", end_time-start_time

# print "Starting Query3"
# query3 = "SELECT * FROM " + tableName + " WHERE RandString = 'aaa'"
# rdd3 = sqlContext.sql(query3)
# print "Starting Count3"
# start_time = time.time()
# rdd3.count()
# end_time = time.time()
# print "Time 3 took:", end_time-start_time


