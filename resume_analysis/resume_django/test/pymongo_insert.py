from pymongo import MongoClient

import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")


mydb = myclient["resume_data"]
# 创建集合（相当于表）
mycol = mydb["resume_interest"]
mycol.drop()
# 插入数据
# import time
# time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
# result={'姓名':'张红','邮箱':'898008559@qq.com','时间':time}
# mycol.insert_one(result)
#
# for x in mycol.find():
#   print(x)