from pyspark import SparkContext
import itertools
sc = SparkContext("spark://sparkMaster:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log")

# 1. Read data in as pairs of (user_id, item_id clicked on by the user)
pairs = data.map(lambda line: tuple(line.split("\t")))
# 1. pairs: ('1', '3')
# 1. Output example: ('1', '3')
pairs = pairs.distinct()
output = sorted(pairs.collect())
for pair in output:
	print(pair)
	# print("\n")

print ("Print (user, item) pairs done")

# 2. Group data into (user_id, list of item ids they clicked on)
user_items = pairs.groupByKey()
# 2. user_items: ('1', <pyspark.resultiterable.ResultIterable object at 0x7f39563fe668>)
# 2. Output example: 1: 3, 333, 33, 33, 81, 
output = sorted(user_items.collect())
for user, items in output:
	print(user+": ", end='')
	for item in items:
		print(item+", ", end='')
	print("\n")

print ("Print (user, items) pairs done")

# 3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
user_pair = user_items.flatMap(lambda ui: [(ui[0], pair) for pair in list(itertools.combinations(ui[1],2))])
# 3. user_pair: (1, ('333', '33'))
# 3. Output example: 1: ('333', '33')
output = sorted(user_pair.collect())
for user, pair in output:
	print(user+": "+str(pair))

print ("Print (user, item_pair) pairs done")




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