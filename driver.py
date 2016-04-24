from pyspark import SparkContext

sc = SparkContext("spark://sparkMaster:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log")

# 1. Read data in as pairs of (user_id, item_id clicked on by the user)
pairs = data.map(lambda line: line.split("\t"))
# 1. Output example: ['1', '3']
output = pairs.collect()
for pair in output:
	print(pair)
	# print("\n")

print ("Print pairs done")

# 2. Group data into (user_id, list of item ids they clicked on)
user_items = pairs.groupByKey()
# 2. Output example: ['1', '3']
output = user_items.collect()
for user, items in output:
	print(user+"\t")
	for item in items:
		print(item+"\t")
	print("\n")

print ("Print user_items done")

# pages = pairs.map(lambda pair: (pair[1], 1))
# count = pages.reduceByKey(lambda x,y: x+y)


# output = pairs.collect()
# for pair in output:
# 	print(pair)
# 	print("\n")
    # print ("page_id %s count %d" % (page_id, count))
  
# print ("Print pairs done")

# 1. Read data in as pairs of (user_id, item_id clicked on by the user)
# 2. Group data into (user_id, list of item ids they clicked on)
# 3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
# 4. Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2) 
# 5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
# 6. Filter out any results where less than 3 users co-clicked the same pair of items