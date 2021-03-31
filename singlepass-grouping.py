import time

from pymongo import MongoClient
from collections import Counter

import math
import json
import re

WORD = re.compile(r'\w+')

b = time.time()
client = MongoClient('127.0.0.1', 27017)  # is assigned local port
dbName = "TwitterDump"  # set-up a MongoDatabase
db = client[dbName]
collName = 'Drump'  # here we create a collection
collection = db[collName]  # This is for the Collection  put in the DB

bol = False
count = 0
result = collection.find({"retweet": bol}).limit(5000)


class Classification(object):
    clusterList = []

    def __init__(self):
        self.clusterCounter = 0

    def addCluster(self, textId, text, date, createDate, verified, followers, profile, cid):
        clusterInfo = [textId, text, date, createDate, verified, followers, profile, cid]
        self.clusterList[cid].append(clusterInfo)

    def createCluster(self, textId, text, date, createDate, verified, followers, profile):
        clusterInfo = [textId, text, date, createDate, verified, followers, profile, self.clusterCounter]
        groupClusterCom = []
        groupClusterCom.append(clusterInfo)
        self.clusterList.append(groupClusterCom)

    def getCluster(self, textId, text, date, createDate, verified, followers, profile):
        maxSim = 0
        cid = 0

        if self.clusterCounter == 0:
            self.createCluster(textId, text, date, createDate, verified, followers, profile)
            self.clusterCounter += 1
        else:
            # try:
                for cluster1 in range(0, len(self.clusterList)):
                    sim = self.computeSimilarity(text, cluster1)
                    if sim > maxSim:
                        maxSim = sim
                        cid = cluster1

                if maxSim < 0.6:
                    self.createCluster(textId, text, date, createDate, verified, followers, profile)
                    self.clusterCounter += 1
                else:
                    self.addCluster(textId, text, date, createDate, verified, followers, profile, cid)
            # except Exception as e:
            #     print(e)
        return

    def computeSimilarity(self, text_ori, sid):
        avgSim = 0
        coText = text_ori
        for x in self.clusterList[sid]:
            vector1 = self.text_to_vector(x[1])
            vector2 = self.text_to_vector(coText)
            avgSim += self.get_cosine(vector1, vector2)

        return avgSim/len(self.clusterList[sid])

    def text_to_vector(self, textD):
        words = WORD.findall(textD)
        return Counter(words)

    def get_cosine(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

text = []
textId = []
date = []
createDate = []
verified = []
followers = []
profile = []
for i in result:
    text.append(i['text'])
    textId.append(i['_id'])
    date.append(i['date'])
    createDate.append(i['creatTime'])
    verified.append(i['verifiedStatus'])
    followers.append(i['followers'])
    profile.append(i['profile'])


cluster = Classification()

for k in range(0, len(text)):
    cluster.getCluster(textId[k], text[k], date[k], createDate[k], verified[k], followers[k], profile[k])

print(cluster.clusterList)
print("total cluster:", cluster.clusterCounter)

maxVal = 0
for x in cluster.clusterList:
    for i in range(0, len(x)):
        if len(x) > maxVal:
            maxVal = len(x)

print("max cluster size", maxVal)

startRankTime = time.time()

print(startRankTime-b)

with open("textGrouped.json", 'w', encoding="utf-8") as g1:
    json.dump(cluster.clusterList, g1, ensure_ascii=False)

