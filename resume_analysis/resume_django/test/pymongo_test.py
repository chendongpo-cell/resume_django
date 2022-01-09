from pymongo import MongoClient

import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")


#数据库
db_collection=myclient['resume_data'] # 每个数据库包含多个集合，根据集合名称获取集合对象（Collection）

#获取数据库中所有的 collection 名称
collection_names = db_collection.collection_names()
print(collection_names)


#首先获取集合，也就是表,然后使用drop()方法删除
table=db_collection['resume_json']
table.drop()

#获取集合
table=db_collection['resume_interest']
# 查询一条数据,我们可以使用 find_one() 方法来查询集合中的一条数据
x = table.find_one({"姓名": "陈坡"})
if x:
    print('存在')
else:
    print('不存在')
print(x)
print('----------------------------------------------------------------------')

# 查询集合中所有数据,find() 方法可以查询集合中的所有数据，类似 SQL 中的 SELECT * 操作。
for x in table.find():
  print(x['姓名'])

# 查询指定字段的数据,我们可以使用 find() 方法来查询指定字段的数据，将要返回的字段对应值设置为 1。
for x in table.find({}, {"_id": 0, "name": 1, "alexa": 1}):
    print(x)

# 根据指定条件查询,我们可以在 find() 中设置参数来过滤数据。以下实例查找 name 字段为 "陈东" 的数据：
myquery = {"姓名": "陈东坡"}

mydoc = table.find(myquery)
if mydoc.count():
    print('查询到')
else:
    print('没有结果')
print(mydoc)
for x in mydoc:
    if x:
        print('查询到')
    else:
        print('没有结果')