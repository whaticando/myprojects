from django.test import TestCase

# Create your tests here.
'''
python中的可变数据类型：列表，字典，集合
python中的不可变数据类型：字符串，数字，元祖
所谓不可变就是说, 我们不能改变这个数据在内存中的值, 所以当我们改变这个变量的赋值时, 
只是在内存中重新开辟了一块空间, 将这一条新的数据存放在这一个新的内存地址里,
 而原来的那个变量就不在引用原数据的内存地址而转为引用新数据的内存地址了。
 数字又分为bool int float complex等
'''

# d = {1:{"xxx":[1,2,3]},2:{'xxx':[4,5,6]},3:{'xxx':[7,8,9]}}
#
# d[1]['xxx'].append(d[2]['xxx'])
# d[2]['xxx'].append(d[3]['xxx'])
# print(d)

d = {1:'222',2:'333'}
d = {value:key for key,value in d.items()}
print(d)

comment_list=[
    {'id':1,"content":'111','Pid':None},
    {'id': 2, "content": '222', 'Pid': None},
    {'id': 3, "content": '333', 'Pid': None},
    {'id': 4, "content": '444', 'Pid': None},
    {'id': 5, "content": '555', 'Pid': 1},
    {'id': 6,"content":'666','Pid':1},
    {'id': 7, "content": '777', 'Pid': 4},
    {'id': 8, "content": '888', 'Pid': None},
]

#
# for obj in comment_list:
#     obj['children_list'] = []

# print(comment_list)


ret= []
for obj in comment_list:
    pid = obj["Pid"]
    if pid:
        for i in comment_list:
            if i['id'] == pid:
                i["children_list"].append(obj)
    else:
        ret.append(obj)
print(ret)
