# Twitter-crawler

## Coding Environment:
Python version:3.8.3 
tweepy version:3.10.0  
pymongo version:3.11.2  
emoji version:0.6.0  

## Twitter streaming API and REST API crawler:
By open file  **<u>`streamCrawler.py`</u>**  
By open file  **<u>`countstream.py`</u>** make streaming data statistics.
The streaming data will store as `./original_data/data.json`  
The rest data will store as `./original_data/rest.json`  
By open file  **<u>`hybridcount.py`</u>** make hybrid structure data statistics.  

## Twitter grouping methods:
Singlepass algorithm:By open file **<u>`singlepass-grouping.py`</u>** the grouped text will store as `./original_data/textGrouped.json`  
LSH-Kmeans algorithm:By open file **<u>`lshKmeans.py`</u>**  
PCA-Kmeans algorithm:By open file **<u>`KmeansPCA.py`</u>**  

## Word and group priority: 
Reading the data in `./original_data/textGrouped.json` ,ranking group and stored as `./textRanked.json`

## Media downloading method:
By open file **<u>`downloadMedia.py`</u>**  , store the video file in local root.
