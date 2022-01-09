from pymongo import MongoClient

import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")


#数据库
db_collection=myclient['mongo_test'] # 每个数据库包含多个集合，根据集合名称获取集合对象（Collection）


#



table=db_collection['cdp']


result={'姓名':'陈东坡','性别':'男','年龄':'18','家庭地址':'上海市','爱好':'乒乓球','身高':'175'}
table.insert_one(result)

#获取数据库中所有的 collection 名称
# collection_names = db_collection.collection_names()
# print(collection_names)

for x in table.find():
  print(x)