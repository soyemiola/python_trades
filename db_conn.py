import pymongo

url = "" # add mongodb connection string

client = pymongo.MongoClient(url)

db = client['Trading']