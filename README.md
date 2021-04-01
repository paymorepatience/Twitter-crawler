# Twitter-crawler

## coding environment:
Python version:3.8.3 (default, Jul  2 2020, 17:30:36)  [MSC v.1916 64 bit (AMD64)]  
tweepy version:3.10.0  
pymongo version:3.11.2  
emoji version:0.6.0  

## Twitter streaming API and REST API crawler:
By open file  **<u>`streamCrawler.py`</u>**  
By open file  **<u>`countstream.py`</u>** make statistics .
The streaming data will store as `./original_data/data.json`  
The rest data will store as `./original_data/rest.json`  

## Twitter grouping methods:
Singlepass algorithm:By open file **<u>`singlepass-grouping.py`</u>** the grouped text will store as `./original_data/textGrouped.json`  
LSH-Kmeans algorithm:By open file **<u>`lshKmeans.py`</u>**  
PCA-Kmeans algorithm:By open file **<u>`KmeansPCA.py`</u>**  
