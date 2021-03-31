from random import random
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from pymongo import MongoClient
from numpy import mean
import re
import numpy as np
import sys
import time

def distEclud(vecA, vecB):
    return np.sqrt(np.sum(np.power(vecA - vecB, 2)))

def randCent(dataSet, k):
    """
    随机生成k个聚类中心

    Args:
        dataSet: 数据集
        k: 簇数目
    Returns:
        centroids: 聚类中心矩阵
    """
    m, _ = dataSet.shape
    # 随机从数据集中选几个作为初始聚类中心
    centroids = dataSet.take(np.random.choice(80,k), axis=0)
    return centroids

def kMeans(dataSet, k, maxIter=15):
    """
    K-Means

    Args:
        dataSet: 数据集
        k: 聚类数
    Returns:
        centroids: 聚类中心
        clusterAssment: 点分配结果
    """
    # 随机初始化聚类中心
    centroids = randCent(dataSet, k)
    init_centroids = centroids.copy()

    m, n = np.shape(dataSet)

    # 点分配结果： 第一列指明样本所在的簇，第二列指明该样本到聚类中心的距离
    clusterAssment = np.mat(np.zeros((m, 2)))

    # 标识聚类中心是否仍在改变
    clusterChanged = True

    # 直至聚类中心不再变化
    iterCount = 0
    while clusterChanged and iterCount < maxIter:
        iterCount += 1
        clusterChanged = False
        # 分配样本到簇
        for i in range(m):
            # 计算第i个样本到各个聚类中心的距离
            minIndex = 0
            minDist = np.inf
            for j in range(k):
                dist = distEclud(dataSet[i, :], centroids[j, :])
                if (dist < minDist):
                    minIndex = j
                    minDist = dist
            # 任何一个样本的类簇分配发生变化则认为变化
            if (clusterAssment[i, 0] != minIndex):
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist ** 2

        # 刷新聚类中心: 移动聚类中心到所在簇的均值位置
        for cent in range(k):
            # 通过数组过滤获得簇中的点
            ptsInCluster = dataSet[np.nonzero(
                clusterAssment[:, 0].A == cent)[0]]
            if ptsInCluster.shape[0] > 0:
                # 计算均值并移动
                centroids[cent, :] = np.mean(ptsInCluster, axis=0)
    return centroids, clusterAssment, init_centroids


def min_max_normalize(data):
    for j in range(len(data)):
        min_x = min(data[j])
        max_x = max(data[j])
        for i in range(len(data[j])):
            data[j][i] = (data[j][i] - min_x) / (max_x - min_x)


def get_minhash(data2, n_hashes, random_strings):
    minhash_row = []
    for i in range(n_hashes):
        minhash = sys.maxsize
        for shingle in data2:
            hash_candidate = abs(hash(shingle + random_strings[i]))
            if hash_candidate < minhash:
                minhash = hash_candidate
        minhash_row.append(minhash)
    return minhash_row


if __name__ == '__main__':
    b = time.time()
    client = MongoClient('127.0.0.1', 27017)  # is assigned local port
    dbName = "TwitterDump"  # set-up a MongoDatabase
    db = client[dbName]
    collName = 'Drump'  # here we create a collection
    collection = db[collName]  # This is for the Collection  put in the DB
    numHASH = 50
    bucket = 6
    documents = []
    bol = True
    count = 0
    result = collection.find({"retweet": bol}, {"text": 1, "date": 1}).limit(4000)

    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = get_stop_words('en')
    for i in result:
        documents.append(i['text'])

    Rstrings = [str(random()) for _ in range(numHASH)]
    hashResult = []
    for row in documents:
        rec = row.lower()
        rec1 = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', rec, flags=re.MULTILINE)
        tokens = tokenizer.tokenize(rec1)
        stopped_tokens = [i for i in tokens if not i in en_stop]
        minhash_row = get_minhash(stopped_tokens, numHASH, Rstrings)
        hashResult.append(minhash_row)

    clusterNum = 10
    hashResult = np.array(hashResult)
    centroids, clusterAssment, init_centroids = kMeans(hashResult, clusterNum)
    print("total tweets:", len(clusterAssment))
    # for x in clusterAssment:
    #     len(x)
    count1 = 0
    resultCount = []
    for i in range(0, clusterNum):
        resultCount.append(0)

    for i in clusterAssment:
        for k in range(0, clusterNum):
            if i[0, 0] == k:
                resultCount[k] += 1
    a = time.time()

    print("time:", a-b)

    print("cluster", resultCount)
    print("max", max(resultCount))
    print("min", min(resultCount))
    print("avg", mean(resultCount))
