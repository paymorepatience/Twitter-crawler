from pymongo import MongoClient

# this is to setup local Mongodb
client = MongoClient('127.0.0.1',27017) #is assigned local port
dbName = "TwitterDump" # set-up a MongoDatabase
db = client[dbName]
collName = 'Drump' # here we create a collection
collection = db[collName] #  This is for the Collection  put in the DB

data = []

retweetSet = []
quoteSet = []
photoSet = []
verifiedSet = []
geoenabledSet = []
locationPlaceSet = []
videoSet = []
bol = True
total = collection.find()
retweetSet1 = collection.find({"retweet": bol})
quoteSet1 = collection.find({"quote": bol})
photoSet1 = collection.find({"photoAddress": {'$ne': None}})
verifiedSet1 = collection.find({"verifiedStatus": bol})
geoenabledSet1 = collection.find({"geoenabled": bol})
locationPlaceSet1 = collection.find({'$or': [{"location": {'$ne': None}}, {"place_name": {'$ne': None}}]})
videoSet1 = collection.find({'videoAddress': {'$ne': None}})

for i in total:
    data.append(i)

for i in retweetSet1:
    retweetSet.append(i)

for i in quoteSet1:
    quoteSet.append(i)

for i in photoSet1:
    photoSet.append(i)

for i in verifiedSet1:
    verifiedSet.append(i)

for i in geoenabledSet1:
    geoenabledSet.append(i)

for i in locationPlaceSet1:
    locationPlaceSet.append(i)

for i in videoSet1:
    videoSet.append(i)



print("totals:", len(data))
print("retweet:", len(retweetSet))
print("quote:", len(quoteSet))
print("photo:", len(photoSet))
print("video:", len(videoSet))
print("verified:", len(verifiedSet))
print("geo-tagged:", len(geoenabledSet))
print("place or location:", len(locationPlaceSet))


