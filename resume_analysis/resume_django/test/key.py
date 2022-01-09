# aaa="四级"
# if "四" in aaa:
#     print("你好")
#
# aa=[1,2,4,5]
#
# def jjj(aa):
#
#     for i in aa:
#         if i ==4:
#             return i
#         print(i)
# jjj(aa)
#
#
# a='您好海拔，你'
# print(len(a))
# a=a[0:6]
# print(a)
#
#
# end=''
# if end:
#     print("你好")
#当前文件的路径
# import os
#
# pwd = os.getcwd()
# #当前文件的父路径
# print(pwd)
# father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
# print(father_path)
# #当前文件的前两级目录
# grader_father=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
# print(grader_father)
# import  re
# cc_re='年|时'
# str='工作'
# cc_re=re.compile(cc_re)
# c=re.search(cc_re,str)
# # print(c)
# list_test=[10,12,14,16,18,19,28]
# print(list_test[-6:])
# 导入time模块
import time
# 格式化时间戳为本地的时间
# print(time.localtime(time.time()))
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))