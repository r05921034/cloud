from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import json
import gzip
import pymongo
url="http://data.taipei/youbike"
a=Request(
    url,
    headers={
        "Accept-Encoding": "gzip"})
response = urlopen(a)
gzipFile = gzip.GzipFile(fileobj=response)
b=gzipFile.read().decode('utf-8')
#c=gzip.decompress(response.read())
output=json.loads(b)
print(output)


'''
html= urlopen("http://data.taipei/youbike").read().decode('utf-8')
reponse=json.loads(html)
'''
#print(reponse)

#bs=BeautifulSoup(html)


'''
for link in bs.findAll("a"):
	if 'href' in link.attrs:
		print(link.attrs['href'])
'''
