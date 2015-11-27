
#Use APRIORI for mining association rules
#
#TODO: Create window of operation and next k operations, itemset is all items
#in the window
#
def createAssociations():
	#Each association takes the form X -> Y
	#One SQL operation can appear in multiple X -> Y rules
	#Resolution: Choose rule X -> Y with highest confidence s.t. 
	#Y contains SQL Operation
	#
	#Then map each X to its set, Y, of associated SQL operations

#Given relevant columns in an RDD and an operation, return relevant output
#
def execRddOp(sqlRDD, rddOp):
	#TODO: Map rddOperation (function lambda?) to actual execution

#Given a sql operation and the (cached) rdd that includes the relevant
#columns for this query, return filtered RDD of relevant columns
#
def filterRelevantColumns(sqlOp, fullRDD):
	#TODO: Map SQL operation to relevant filter for columns, return column

#Relevant columns for sqlOp is cached within an RDD somewhere, need to 
#(1) Retrieve the cached RDD
#(2) Filter out irrelevant columns
#
def getCachedRdd(sqlOp):
	#In which RDD is the info hiding?
	#
	fullRDD = lookup[sqlOp]

	return filterRelevantColumns(sqlOp, fullRDD)

#Cache SQL operation data & all relevant information
#
def cacheSqlOp(sqlOp):
	#TODO: For all associated SQL operations, cache relevant columns in one RDD
	#TODO: Map each associated SQL operation to cached RDD in lookup[]

#Determine whether or not to cache data in a SQL operation
#
def shouldCache(sqlOp):
	#TODO: Define parameters for what determines caching

def onReceive(sqlOp, rddOp):
	#If it's frequent enough to gain something from caching
	#
	if (shouldCache(sqlOp)):
		cacheSqlOp(sqlOp)

	#Get RDD from SQL operation
	#
	if isCached(sqlOp):
		#Get RDD if already cached
		#
		sqlRDD = getCachedRdd(sqlOp)
	else:
		#Otherwise just directly query
		#
		sqlRDD = sc.sql(sqlOp)

	#Return result of RDD operation
	#
	return execRddOp(sqlRDD, rddOp)
