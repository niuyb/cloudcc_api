#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/28 17:05
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
import sys,os

from script.data_config import ORDER_DETAIL_DICT, ORDER_DETAIL_TABLE_STRING, ORDER_TABLE_STRING

path1 = os.path.abspath('/var/www/cloudcc_api')
sys.path.append(path1)

from multiprocessing import Process

import pymysql

import pandas as pd

from public.utils import engine
from settings import settings
from settings.config import ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD

pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)# 展示所有列

def get_conn():
    host = "192.168.185.129"
    user = "nyb"
    passwd = "nyb123"
    db = "yydw"
    port = 3306
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        db=db,
        port=port,
        charset='utf8')
    # 获得游标
    cur = conn.cursor()


    return cur, conn

def get_repeat(sql_table):
        new_data = engine(settings.db_new_data)
        # try:
        sql_string = """ select crm_id from {} """.format(sql_table)
        cc_df = pd.read_sql_query(sql_string,new_data)
        print(cc_df.shape)
        delete_df = cc_df.drop_duplicates(keep=False)
        print(delete_df.shape)

        keep_df = cc_df.drop_duplicates(keep="first")
        print(keep_df.shape)

        id_df=delete_df.append(keep_df).drop_duplicates(keep=False)
        print(id_df.shape)
        print(id_df)
        new_data.close()


def delete_repeat(sql_table,sql_table_string):

    new_data = engine(settings.db_new_data)

    sql_string = """ select * from {} """.format(sql_table)
    cc_df = pd.read_sql_query(sql_string, new_data)
    cc_df = cc_df.drop_duplicates(keep="first")

    print(cc_df.shape)

    cc_df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()
    sql_remarks = sql_table_string.format(sql_table)
    cur.execute(sql_remarks)
    cur.close()
    conn.close()
    new_data.close()



if __name__ == "__main__":

    # get_repeat("order_detail_back_copy2")


    delete_repeat("order_detail_back_copy1",ORDER_DETAIL_TABLE_STRING)
    # delete_repeat("order_back_copy1",ORDER_TABLE_STRING)












