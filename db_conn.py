import pymongo

url = "mongodb+srv://test:test1234@djangodb.mcqqld9.mongodb.net/"

client = pymongo.MongoClient(url)

db = client['Trading']