# plist='武武汉汉轻轻工工大大学学'
#
# b = list(set(plist))
# b.sort(key=plist.index)
# print(''.join(b))


# time='2014.6'
# print(time.replace('-','.'))

# mmm='————————'
# mmmm=mmm.replace('——','')
# print(len(mmmm))
# num = 5
# if num >= 3:            # 判断num的值
#     print ('boss')
# elif num >= 2:
#     print ('user')
# elif num == 1:
#     print ('worker')
# elif num < 0:           # 值小于零时输出
#     print ('error')
# else:
#     print ('roadman')     # 条件均不成立时输出
#
# if num>=4:
#     print('你好')

# import re
# str='186-3963-1885'
# bbb=re.sub('[^.^-^_^-^0-9]','.',str)
# print(bbb)
# aaa = [i for i in re.sub('[^.^-^_^-^0-9]','.',str).split('.') if i != '']
# print(''.join(aaa))

# print(100//2)
import datetime
print(type(datetime.datetime.now().year))
if '-'=='-':
    print('1')