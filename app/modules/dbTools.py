#dbTools
#Database and data handling logic module for inventoryApp

import pymongo
import modules.config as config

client = pymongo.MongoClient(config.dbString)
db = client[config.dbName]
stacks = db['stacks']
locations = db['locations']
items = db['items']


class stack:

    def __init__(self, part, qty, batch, expiration, unit, location):
        self.partNumber=part #string
        self.qty = qty #float
        self.batch = batch #string
        self.expiration = expiration #datetime or zero for non expiring
        self.unit = unit #string
        self.location = location #string

    def updateQty(self, amount):
        self.qty += amount
    
    def pushStackRecord(self, coll):
        print("creating stack record....")
        rec = {
            'partNumber': self.partNumber,
            'qty': self.qty,
            'unit': self.unit,
            'batch': self.batch,
            'expiration': self.expiration,
            'location' : self.location
        }
        print("Pushing record....")
        x = coll.insert_one(rec)
        print("Push Complete....")

class item:
    def __init__(self, partNum, description, expiration, unit):
        self.partNum = partNum #string
        self.description = description #string
        self.expiration = expiration #datetime or zero for non expiring
        self.unit = unit #string

    def pushItemRecord(self, coll):
        print("creating item record....")
        rec = {
            'partNumber': self.partNum,
            'description': self.description,
            'expiration' : self.expiration,
            'unit' : self.unit
        }
        print("Pushing record....")
        x = coll.insert_one(rec)
        print("Push Complete....")
        

def getStockList(query):
    if query == None:
        res = list(stacks.find())
    else:
        res = list(stacks.find({"$or":[{"partNumber": query}, {"batch": query}, {"location": query}]}))
    
    return res

def getItemList(query):
    if query == None:
        res = list(items.find())
    else:
        res = list(items.find({"$or":[{"partNumber": query}, {"description": query}]}))
    
    return res

def getLocationList(query):
    if query == None:
        res = list(locations.find())
    else:
        res = list(locations.find({"locName": query}))
    
    return res