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
import sys
import importlib
importlib.reload(sys)
import os
path1 = os.path.abspath('/var/www/cloudcc_api')
sys.path.append(path1)


import hashlib
import json
import random
from multiprocessing import Process,Queue

import numpy as np
import pymysql

import time
from datetime import datetime
import pandas as pd
import requests

from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.utils import engine, list_to_sql_string
from script.data_config import ORDER_DICT, ACCOUNT_DICT, OPPORTUNITY_DICT, USER_DICT, MICROPOST_DICT, \
    MICROPOST_CLOUMNS_ORDER, MICROPOST_TABLE_STRING, ACCOUNT_API_NAME, OPPORTUNITY_API_NAME, OPPORTUNITY_SQL_TABLE, \
    ACCOUNT_SQL_TABLE, USER_SQL_TABLE
from script.data_utils import create_id
from settings import settings
from settings.config import ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD

pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)


"""
order_id 生成规则

年份取后两位

"ZO" + md5('order_name + timestamp')+ index

"""


class Order_Data():
    def __init__(self):

        self.access_url  = ''
        self.binding = ''
        self.cloudcc_object="getChatters01"
        self.sql_table= "micropost"
        self.sql_mapping= MICROPOST_DICT

        # self.one_times_num = 1000
        # self.sql_index_list=[]
        self.columns_order=MICROPOST_CLOUMNS_ORDER
        self.sql_table_string = MICROPOST_TABLE_STRING
        self.account_sql_table= ACCOUNT_SQL_TABLE
        self.opportunity_sql_table=OPPORTUNITY_SQL_TABLE
        self.user_table = USER_SQL_TABLE

        self.cc_micropost_url= "https://k8mm3cmt3235c7ed72cede6e.cloudcc.com/distributor.action?"

        self.catch_type=["account","opportunity"]
        self.type={"001":"account","002":"opportunity"}



    # def get_user(self):
    #     new_data = engine(settings.db_new_data)
    #     sql = """ select crm_id from user_back """
    #     df = pd.read_sql_query(sql, new_data)

    def get_conn(self):
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

        return cur,conn


    def get_micro_post(self):
        new_data = engine(settings.db_new_data)
        sql = """ select crm_id from user_back """
        df = pd.read_sql_query(sql, new_data)

        for row in df.itertuples():
            # index = getattr(row, 'Index')
            user_id = getattr(row, 'crm_id')
            self.get_cc_micropost(user_id,new_data)
            print(user_id)




    def get_cc_micropost(self,user_id,new_data):
        try:
            access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
            binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
        except:
            print("获取binding失败,请检查配置")
            return None


        datas = {"serviceName": self.cloudcc_object, "binding": binding,
                 "data": {"queryType": "zone", "userId": user_id, "limit":500}}

        datas['data'] = json.dumps(datas['data'])
        response = requests.post(self.cc_micropost_url, data=datas).text
        response_data = json.loads(response)
        res_data = response_data["data"]

        self.change_data(res_data,new_data)


    def change_data(self,data,new_data):

        cc_df = pd.DataFrame(data)
        ccdf_name_list = list(self.sql_mapping.keys())
        cc_df = cc_df[ccdf_name_list]
        cc_df = cc_df.rename(columns=self.sql_mapping)

        # 本次操作的cc id
        operate_list = cc_df["crm_id"].tolist()
        operate_str = list_to_sql_string(operate_list)
        local_sql = """ select id,crm_id from `{}` where crm_id in ({})""".format(self.sql_table, operate_str)
        local_df = pd.read_sql_query(local_sql, new_data)
        # 合并保留id
        local_merge_df = local_df[["id", "crm_id"]]
        cc_df = pd.merge(cc_df, local_merge_df, how='left', on="crm_id")
        # 本次操作local数据库id
        local_list = cc_df["crm_id"].tolist()
        local_str = list_to_sql_string(local_list)


        local_account_sql = """ select id,crm_id  from `{}` """.format(self.account_sql_table)
        local_account_df = pd.read_sql_query(local_account_sql, new_data)
        local_opp_sql = """ select id,crm_id  from `{}`""".format(self.opportunity_sql_table)
        local_opp_df = pd.read_sql_query(local_opp_sql, new_data)

        index_sql = """ select count(id) as nums from {} """.format(self.sql_table)
        id_index = pd.read_sql_query(index_sql, new_data)["nums"].tolist()[0]
        for row in cc_df.itertuples():
            index = getattr(row, 'Index')
            target_id = str(getattr(row, 'target_id'))
            object_sql_table = self.type.get(str(target_id[:3]),None)
            if object_sql_table:
                target_id = getattr(row, 'target_id')
                id = getattr(row, 'id')
                if isinstance(id,str):
                    print("AAAAAAAAAA")
                    pass
                else:
                    print("DDDDDDDDDDD")
                    target_name = getattr(row, 'target_name')
                    created_at = getattr(row, 'created_at')
                    id = create_id(target_name, created_at, id_index)
                    cc_df.at[index, 'id'] = id
                    id_index+=1

                if object_sql_table == "account":
                    local_target_id = local_account_df.loc[local_account_df["crm_id"] == target_id,"id"].tolist()
                    if local_target_id:
                        cc_df.at[index, 'target_id'] = local_target_id[0]
                        cc_df.at[index, 'target_object'] = "account"
                else:
                    local_target_id = local_opp_df.loc[local_opp_df["crm_id"] == target_id, "id"].tolist()
                    if local_target_id:
                        cc_df.at[index, 'target_id'] = local_target_id[0]
                        cc_df.at[index, 'target_object'] = "opportunity"

            else:
                cc_df=cc_df.drop(labels=index)   # axis默认等于0，即按行删除，这里表示按行删除第0行


        local_user_sql = """select `id` as local_owner_id ,crm_id as created_by from {}""".format(self.user_table)
        local_user_df = pd.read_sql_query(local_user_sql, new_data)
        cc_df = pd.merge(cc_df, local_user_df, how='left', on="created_by")
        cc_df = cc_df.drop(["created_by"], axis=1)
        cc_df = cc_df.rename(columns={"local_owner_id": "created_by"})

        print(cc_df)
        self.inster_sql(cc_df,local_str,new_data)




    def inster_sql(self,df,local_str,new_data):
        cur, conn = self.get_conn()
        # 删除本次操作的所有local id
        delete_sql = """ delete from {} WHERE crm_id in ({}) """.format(self.sql_table, local_str)
        cur.execute(delete_sql)
        conn.commit()
        # 入库操作
        df = df[self.columns_order]
        df.to_sql(self.sql_table, new_data, index=False, if_exists="append")
        sql_remarks = self.sql_table_string.format(self.sql_table)
        cur.execute(sql_remarks)
        cur.close()
        conn.close()
        new_data.close()



if __name__ == "__main__":
    o = Order_Data()


    # o.get_micro_post()
    new_data = engine(settings.db_new_data)

    o.get_cc_micropost("0052017BE8702F1PIi4j",new_data)











