import math
import re
import numpy as np
from pymongo import MongoClient
from numpy.linalg import eig
from sklearn.decomposition import PCA
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from numpy import mean
import time

client = MongoClient('127.0.0.1', 27017)  # is assigned local port
dbName = "TwitterDump"  # set-up a MongoDatabase
db = client[dbName]
collName = 'Drump'  # here we create a collection
collection = db[collName]  # This is for the Collection  put in the DB

doc_set = []
bol = False
count = 0
result = collection.find({"retweet": bol}, {"text": 1, "date": 1}).limit(4000)

time_set = []
id_set = []
for x in result:
    doc_set.append(x['text'])
    time_set.append(x['date'])
    id_set.append(x['_id'])

tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
text = []



k = doc_set
rekc = []

text1 = []

# tfidf = TfidfVectorizer(stop_words=STOP_WORDS)
#
# response = tfidf.fit_transform(doc_set)
# feature_names = tfidf.get_feature_names()
# for col in response.nonzero()[1]:
#     if response[0, col] != 0:
#         print(feature_names[col], ' - ', response[0, col])



# for i in k:
#     text1.append(i.split(" "))

for i in k:
    raw = i.lower()
    raw = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', raw, flags=re.MULTILINE)
    # tokens = raw.split(" ")
    tokens = tokenizer.tokenize(raw)
    stopped_tokens = [i for i in tokens if not i in en_stop]
    if len(stopped_tokens) == 0:
        stopped_tokens = 'emptytweet'
    # print(stopped_tokens)
    text1.append(stopped_tokens)
# count4 = 0
# count5 = 0
# for i in text1:
#     if len(i) == 0:
#         count4 += 1
#     count5 += 1


wordSet = []
wordSet1 = []

for i in text1:
    wordSet = list(set(wordSet).union(set(i)))
for i in range(0, len(text1)):
    wordSet1.append(dict.fromkeys(wordSet, 0))

for sentence in range(0, len(text1)):
    for word in text1[sentence]:
        wordSet1[sentence][word] += 1


def computeTF(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

tfresult = []

for x in range(0, len(text1)):
    x = computeTF(wordSet1[x], text1[x])
    tfresult.append(x)

def computeIDF(docList):
    idfDict = {}
    N = len(docList)

    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))

    return idfDict


idfresult = computeIDF(wordSet1)

def computeTFIDF(tfBow, idfs, cId):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = [val*idfs[word], id_set[cId], time_set[cId]]
    return tfidf

tfidfResult = []

for x in range(0, len(text1)):
    tfidfResult.append(computeTFIDF(tfresult[x], idfresult, x))

dataset = []
for i in range(0, len(tfidfResult)):
    groupInfo = []
    for j in tfidfResult[i].values():
        groupInfo.append(j[0])
    dataset.append(groupInfo)
# print(dataset)

#Calculate the Euclidean distance between the variables
def distEclud(vecA, vecB):
    return np.sqrt(np.sum(np.power(vecA - vecB, 2)))


def randCent(dataSet, k):

    m, _ = dataSet.shape

    centroids = dataSet.take(np.random.choice(80,k), axis=0)
    return centroids

def kMeans(dataSet, k, maxIter=15):

    centroids = randCent(dataSet, k)
    init_centroids = centroids.copy()

    m, n = np.shape(dataSet)

    clusterAssment = np.mat(np.zeros((m, 2)))


    clusterChanged = True


    iterCount = 0
    while clusterChanged and iterCount < maxIter:
        iterCount += 1
        clusterChanged = False

        for i in range(m):

            minIndex = 0
            minDist = np.inf
            for j in range(k):
                dist = distEclud(dataSet[i, :], centroids[j, :])
                if (dist < minDist):
                    minIndex = j
                    minDist = dist

            if (clusterAssment[i, 0] != minIndex):
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist ** 2


        for cent in range(k):

            ptsInCluster = dataSet[np.nonzero(
                clusterAssment[:, 0].A == cent)[0]]
            if ptsInCluster.shape[0] > 0:

                centroids[cent, :] = np.mean(ptsInCluster, axis=0)
    return centroids, clusterAssment, init_centroids


b = time.time()
dataset = np.array(dataset)
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(dataset)

clusterNum = 8
centroids, clusterAssment, init_centroids = kMeans(principalComponents, clusterNum)


print("total tweets:", len(clusterAssment))
# for x in clusterAssment:
#     len(x)
count1 = 0
resultCount = []
for i in range(0, clusterNum):
    resultCount.append(0)

for i in clusterAssment:
    for k in range(0, clusterNum):
        if i[0,0] == k:
            resultCount[k] += 1

a = time.time()

print(a-b)
print("cluster", resultCount)
print("max", max(resultCount))
print("min", min(resultCount))
print("avg", mean(resultCount))
