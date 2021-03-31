from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)  # is assigned local port
dbName = "TwitterDump"  # set-up a MongoDatabase
db = client[dbName]
collName2 = 'Drump1'
collName6 = 'Drump'  # here we create a collection
collection2 = db[collName2]  # This is for the Collection  put in the DB
collection6 = db[collName6]
bol = True

count_rest = collection2.find().count()
count_streaming = collection6.find().count()
result_count = count_rest + count_streaming
id_rest = collection2.find({}, {'_id': 1})

id_streaming = collection6.find({}, {'_id': 1})

rest=[]
streaming=[]
for i in id_rest:
    rest.append(i['_id'])
for j in id_streaming:
    streaming.append(j['_id'])
count = 0
for i in rest:
    print(i)
    for j in streaming:
        print(j)
        if i == j:
            count += 1

print('total amounts of streaming api', count_streaming)
print('total amounts of rest', count_rest)
print('redundant data', count)
result2_1 = collection2.find({"geoenabled": bol}).count()
result6_1 = collection6.find({"geoenabled": bol}).count()
result1 = result2_1 + result6_1
result2_2 = collection2.find({'$or': [{"location": {'$ne': None}}, {"place_name": {'$ne': None}}]}).count()
result6_2 = collection6.find({'$or': [{"location": {'$ne': None}}, {"place_name": {'$ne': None}}]}).count()
result2 = result2_2 + result6_2
result2_3 = collection2.find({"media": "photo"}).count()
result6_3 = collection6.find({"media": "photo"}).count()
result3 = result2_3 + result6_3
result2_4 = collection2.find({'videoLinks': {'$ne': None}}).count()
result6_4 = collection6.find({'videoLinks': {'$ne': None}}).count()
result4 = result2_4 + result6_4
result2_5 = collection2.find({"verified": bol}).count()
result6_5 = collection6.find({"verified": bol}).count()
result5 = result2_5 + result6_5
result2_6 = collection2.find({"retweet": bol}).count()
result6_6 = collection6.find({"retweet": bol}).count()
result6 = result2_6 + result6_6
result2_7 = collection2.find({"quote": bol}).count()
result6_7 = collection6.find({"quote": bol}).count()
result7 = result2_7 + result6_7

print("total amounts:", result_count)
print("tweets with geo-tag :", result1)
print("tweets with locations/Place Object:", result2)
print("Tweets with images:", result3)
print("Tweets with videos:", result4)
print("tweets verified:", result5)
print("Tweets with retweets:", result6)
print("Tweets with quotes:", result7)