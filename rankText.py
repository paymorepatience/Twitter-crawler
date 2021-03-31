import json
import time

with open('textGrouped.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# def computeScore(age, followers, verified, profile):
    # timeStart = time.mktime(time.strptime(age, "%a %b %d %H:%M:%S +0000 %Y"))
    # nowTime = time.time()
    # gapTime = nowTime-timeStart
    # ageTime = int(gapTime // (24 * 60 * 60))
    # print(ageTime)

cout0 = 0
cout = 0
data_set = []
mark_set = []
text_set = []
follower_set = []
age_set = []
verified_set = []
profile_set = []
avgClass = []

def scoreCompute(ageVal, followerVal, verifiedVal, profileVal):
    dayMark = 0
    followerMark = 0
    verifiedMark = 0
    profileMark = 0

    if ageVal < 1:
        dayMark = 0.05
    elif ageVal < 30:
        dayMark = 0.10
    elif ageVal > 90:
        dayMark = 0.25

    if followerVal < 50:
        followerMark = 0.5
    elif followerVal < 5000:
        followerMark = 1.0
    elif followerVal < 10000:
        followerMark = 1.5
    elif followerVal < 100000:
        followerMark = 2.0
    elif followerVal < 200000:
        followerMark = 2.5
    elif followerVal > 200000:
        followerMark = 3.0

    if verifiedVal:
        verifiedMark = 1.5
    else:
        verifiedMark = 1.0

    if profileVal:
        profileMark = 0.5
    else:
        profileMark = 1
    return dayMark, followerMark, verifiedMark, profileMark

for i in range(0, len(data)):
    groupClass = []
    sumVal = 0
    for j in range(0, len(data[i])):
        groupCol = []
        verifiedVal = data[i][j][4]
        followerVal = data[i][j][5]
        profileVal = data[i][j][6]
        timeArry = time.strptime(data[i][j][3], "%a %b %d %H:%M:%S +0000 %Y")
        ageTime = time.time()-time.mktime(timeArry)
        ageVal = int(abs(ageTime))//24//3600

        dayMark, followerMark, verifiedMark, profileMark = scoreCompute(ageVal, followerVal, verifiedVal, profileVal)
        qualityScore = (dayMark + verifiedMark + followerMark + profileMark)/4
        groupClass.append(qualityScore)
        sumVal += qualityScore

    mark_set.append(groupClass)
    avgClass.append(sumVal/len(data[i]))

for x in range(0, len(mark_set)):
    for i in range(0, len(mark_set[x])):
        if len(mark_set[x]) > 1:
            for j in range(i+1, len(mark_set[x])):
                if mark_set[x][i] > mark_set[x][j]:
                    maxVal = mark_set[x][i]
                    mark_set[x][i] = mark_set[x][j]
                    mark_set[x][j] = maxVal
                    maxSet = data[x][j]
                    data[x][i] = data[x][j]
                    data[x][j] = maxSet


for x in range(0, len(mark_set)):
    for i in range(x+1, len(mark_set)):
        if avgClass[x] >avgClass[i]:
            turn1 = avgClass[x]
            avgClass[x] = avgClass[i]
            avgClass[i] = turn1

            turn2 = mark_set[x]
            mark_set[x] = mark_set[i]
            mark_set[i] = turn2

            turn3 = data[x]
            data[x] = data[i]
            data[i] = turn3

dataFilter = []

for x in data:
    if len(x) > 10:
        dataFilter.append(x)



minSize = len(dataFilter[0])
maxSize = 0
avgSize = 0
for x in dataFilter:
    if len(x) < minSize:
        minSize = len(x)
    if len(x) > maxSize:
        maxSize = len(x)
    avgSize += len(x)


print("Arrange the data within and between groups in ascending order, and delete groups of less than 10 items as noise")
print("total nums group is :", len(dataFilter))
print("filtered group max Size:", maxSize)
print("filtered group min Size:", minSize)
print("filtered group average Size:", avgSize/len(dataFilter))

with open("textRanked.json", 'w', encoding="utf-8") as g1:
    json.dump(dataFilter, g1, ensure_ascii=False)
