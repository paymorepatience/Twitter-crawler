import requests
from pymongo import MongoClient
import re

def download_video(video_links):
    root = '/Users/renjiahui/Desktop/WEB SCIENCE/video'
    for link in video_links:
        file_name = link.split('/')[-1]
        file_name = re.sub(r'\?.*','', file_name)
        print("download process: %s" % file_name)
        r = requests.get(link, stream=True).iter_content(chunk_size=1024 * 1024)
        with open(root + file_name, 'wb') as f:
            for chunk in r:
                if chunk:
                    f.write(chunk)

        print("%s complete!\n" % file_name)
    print("all finish!")
    return


if __name__ == "__main__":
    # this is to setup local Mongodb
    client = MongoClient('127.0.0.1', 27017)  # is assigned local port
    dbName = "TwitterDump"  # set-up a MongoDatabase
    db = client[dbName]
    collName1 = 'Drump'
    collection1 = db[collName1]

    result8 = collection1.find({"videoLinks": {'$ne': None}})
    videoLinks = []
    for x in result8:
        videoLinks.append(x['videoLinks'])
    print(videoLinks)

    download_video(videoLinks)
