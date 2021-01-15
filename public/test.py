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

from public.utils import engine
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
    import urllib
    from urllib import parse
    str1 = """select t0.*, t1.type, t1.name group_name, concat(cast(IFNULL(t2.last_name,'') as char),cast(IFNULL(t2.first_name,'') as char))  username from  tp_std_datatable1share t0 left outer join tp_sys_group t1 on t0.userorgroupid=t1.id left outer join tp_sys_user t2 on t0.userorgroupid=t2.id where parentId='记录id' order by t0.id asc """
    str2 = parse.quote(str1)  # quote()将字符串进行编码
    # str2="%E4%B8%8A%E6%B5%B7%E5%8D%8E%E7%91%9E%E9%93%B6%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89"
    print(str2)
    rawurl = str2
    url = parse.unquote(rawurl)
    print (url)



if __name__ == '__main__':
    # a142021103651973Tp9i

    database = engine(settings.db_new_data)
    sql_string = """ select crm_id,account_name from {} """.format("account_back_copy1")
    cc_df = pd.read_sql_query(sql_string, database)

    sql_string = """ select crm_id,account_name from {} """.format("account_back")
    local_df = pd.read_sql_query(sql_string, database)


    # print(cc_df.shape)
    # delete_df = cc_df.drop_duplicates(keep=False)
    # print(delete_df.shape)
    #
    # keep_df = cc_df.drop_duplicates(keep="first")
    # print(keep_df.shape)

    re_df = cc_df.append(local_df).drop_duplicates(keep=False)

    print(re_df.shape)
    print(re_df)
    database.close()


"""
51042   0012021DB8A6057oehWb  国网河北省电力有限公司保定供电公司
"""




