#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/5 9:54
# 工具：PyCharm
# Python版本：3.7.0

# python 2
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# python 3
# import sys
# import importlib
# importlib.reload(sys)
import datetime
import json

import requests

from public.utils import engine, list_to_sql_string
from settings import settings
import pandas as pd
pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)# 展示所有列



import random  # 导入标准块的random

if __name__ == '__main__1':
    def get_random_code():
        checkcode = ''
        for i in range(4):  # 循环4次
            index = random.randrange(0, 3)  # 生成0-3中的一个数
            if index != i and index + 1 != i:
                checkcode += chr(random.randint(97, 122))  # 生成a-z中的一个小写字母
            elif index + 1 == i:
                checkcode += chr(random.randint(65, 90))  # 生成A-Z中的大写字母
            else:
                checkcode += str(random.randint(1, 9))  # 生成1-9的一个数字

        return checkcode


if __name__ == '__main__1':
    # import urllib
    # from urllib import parse
    # str1="https://support.istarshine.com/DataCount/single_user_activity_count?uid=67358"
    # str2 = parse.quote(str1)  # quote()将字符串进行编码
    # str2="%E5%B1%B1%E8%A5%BF%E7%9C%81%E4%BC%81%E4%B8%9A%E5%8F%91%E5%B1%95"
    # print(str2)
    # rawurl = str2
    # url = parse.unquote(rawurl)
    # print (url)
    s = "你好"
    a= s.encode()
    print(a)

    a = b"\x8d\xad\xdb\xd1\xcf\xab\xb3\x9a\xbc\xef"
    a = b"\xe4\xbd\xa0\xe5\xa5\xbd"
    a = a.decode(encoding='UTF-8')
    print(a)

if __name__ == '__main__1':


    # datas = {"serviceName": "getChatters01", "binding": "CD9E92E35722BF4A43DE3885F76D28E9",
    #          "data": {"queryType": "zone","userId":"0052020A2F256D6Jj7Gr"}}

    datas = {"serviceName": "getChatters01", "binding": "29C6734EF0B5035CEE5385789B63E063",
             "data": {"queryType": "zone","userId":"0052017BE8702F1PIi4j"}}

    # datas = {"serviceName": "getChatters01", "binding": "B98EB2938FC6D03B379E28A5E4DF0E60",
    #          "data": {"queryType": "record","recordId":"bef2021CF6FDCDCz4yUf"}}


    datas['data'] = json.dumps(datas['data'])
    url = "https://k8mm3cmt3235c7ed72cede6e.cloudcc.com/distributor.action?"
    ret = requests.post(url, data=datas)

    print(ret.text)

"""
51042   0012021DB8A6057oehWb  国网河北省电力有限公司保定供电公司
"""



if __name__ =="__main__" :
    nums = 1650
    one_times_num = 1000
    sql_index_list=[]

    if nums % one_times_num > 0:
        num_times = int(nums / one_times_num) + 1
    elif nums % one_times_num == 0:
        num_times = int(nums / one_times_num)
    else:
        num_times = 0

    print(num_times)

    for index in range(num_times):
        start = int(index) * one_times_num
        if index == 0:
            start = 1
        sql_index_list.append(start)

    print(sql_index_list)
