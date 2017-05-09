from pyspark.sql import SparkSession
import pyspark
#from bs4 import BeautifulSoup
#from urllib.request import urlopen,Request
#import json
#import gzip
import pymongo
#from pymongo import MongoClient
from pyspark.sql import SparkSession
my_spark = SparkSession.builder.appName("myApp").config("spark.mongodb.input.uri", "mongodb://127.0.0.1/test.posts").config("spark.mongodb.output.uri", "mongodb://127.0.0.1/test.posts").getOrCreate()
#url="http://data.taipei/youbike"
'''
a=Request(
    url,
    headers={
        "Accept-Encoding": "gzip"})
response = urlopen(a)
gzipFile = gzip.GzipFile(fileobj=response)
b=gzipFile.read().decode('utf-8')
output=json.loads(b)
'''
#my_spark.createOrReplaceTempView("temp")
#client = MongoClient('localhost', 27017)
#spa=spark.createDataFrame(output.json())
spa=my_spark.read.format("com.stratio.datasource.mongodb").options(host="localhost:27017", database="test", collection="posts").load()
spa.printSchema()




'''
db = client.test
posts=db.posts
post=posts.insert_one(output)
'''
