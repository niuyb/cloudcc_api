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



import hashlib
import random
from multiprocessing import Process,Queue

import pymysql

import time
from datetime import datetime
import pandas as pd

from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.utils import engine, list_to_sql_string, time_ms
from script.data_config import ORDER_DICT, ACCOUNT_DICT, OPPORTUNITY_DICT, USER_DICT, ORDER_TABLE_STRING, USER_API_NAME, \
    USER_SQL_TABLE, USER_TABLE_STRING, PRODUCT_LINE_API_NAME, PRODUCT_LINE_TABLE_STRING, PRODUCT_LINE_DICT, \
    PRODUCT_LINE_SQL_TABLE
from script.data_utils import create_id
from settings import settings
from settings.config import ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD

pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)# 展示所有列


"""

"""


class Order_Data():
    def __init__(self):

        # self.new_data = engine(settings.db_new_data)
        self.access_url  = ''
        self.binding = ''
        self.cloudcc_object=PRODUCT_LINE_API_NAME
        self.sql_table= PRODUCT_LINE_SQL_TABLE
        self.sql_mapping= PRODUCT_LINE_DICT
        self.sql_table_string = PRODUCT_LINE_TABLE_STRING

        # self.today = datetime.now().strftime('%Y-%m-%d')
        # print(self.today)
        # self.today = "2021-01-03"
        self.one_times_num = 1000
        self.sql_index_list=[]
        self.process_num = 1

        # self.columns_order = ["id","crm_id","po","entity_type","ownerid","status","account_id","priceid","opportunity_id","created_by","created_at","updated_by","updated_at","amount","discount_amount","contract_status","contract_attribute","contractid","contract_start","contract_end","contract_back_date","total_performance","salerA","salerB","salerC","salerA_amount","salerB_amount","salerC_amount","approve_date","payback_type"]
        # self.ignore_key_list=["id","crm_id"]
        # self.df_list=[]


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

    def deal_df(self,order_df,key,type):
        if type.find(",") >0:
            type_list = type.split(",")
            for type in type_list:
                order_df.loc[order_df[key] == type, key] = ""
        else:
            pass
            order_df.loc[order_df[key] == type, key] = ""
        return order_df

    def merge_df(self,main_df,right_df,user_key,user_crm_key,key,crm_key):
        right_df = right_df.rename(columns={user_key: key,user_crm_key:crm_key})
        main_df = pd.merge(main_df, right_df, how='left', on=crm_key)
        main_df = main_df.drop([crm_key], axis=1)
        return main_df

    def inster_sql(self, df):
        new_data = engine(settings.db_new_data)
        df.to_sql(self.sql_table, new_data, index=False, if_exists="append")
        cur, conn = self.get_conn()
        sql_remarks = self.sql_table_string.format(self.sql_table)
        cur.execute(sql_remarks)
        cur.close()
        conn.close()
        new_data.close()

    def get_cloudcc_order(self,index):

        # self.today = "2020-12-29"
        try:
            self.access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
            self.binding = cloudcc_get_binding(self.access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
        except:
            print("获取binding失败,请检查配置")
            return False

        cur,conn = self.get_conn()
        new_data = engine(settings.db_new_data)

        if index == 1:
            index = 0
        # try:
        sql_string = """ select {} from {}  limit {},{} """
        sql = sql_string.format("*", self.cloudcc_object,index,self.one_times_num)
        data = cloudcc_query_sql(self.access_url, "cqlQuery",self.cloudcc_object, sql, self.binding)
        if data:
            cc_df = pd.DataFrame(columns=list(self.sql_mapping.keys()))
            cc_df = cc_df.append(data,ignore_index=True,sort=False)
            ccdf_name_list = list(self.sql_mapping.keys()) + ["is_deleted"]
            cc_df = cc_df[ccdf_name_list]
            cc_df = cc_df.rename(columns=self.sql_mapping)

            # 本次操作的cc id
            operate_list = cc_df["crm_id"].tolist()
            operate_str = list_to_sql_string(operate_list)
            local_sql = """ select * from `{}` where crm_id in ({})""".format(self.sql_table,operate_str)
            local_df = pd.read_sql_query(local_sql,new_data)
            # 本次操作local数据库id
            local_list = cc_df["crm_id"].tolist()
            local_str = list_to_sql_string(local_list)

            # 删除cc 与 local 中删除的数据
            deleted_list = cc_df.loc[cc_df["is_deleted"] != "0","crm_id"].tolist()
            for deleted_id in deleted_list:
                local_df = local_df.drop(local_df[local_df['crm_id'] == deleted_id].index)
                cc_df = cc_df.drop(cc_df[cc_df['crm_id'] == deleted_id].index)
            print("已删除",len(deleted_list))
            cc_df = cc_df.drop(["is_deleted"],axis=1)

            # 新增 数据
            local_merge_df = local_df[["id","crm_id"]]
            cc_df = pd.merge(cc_df, local_merge_df, how='left', on="crm_id")
            index_sql = """ select count(*) as nums from %s """%(self.sql_table)
            id_index = pd.read_sql_query(index_sql,new_data)["nums"].tolist()[0]
            for row in cc_df.itertuples():
                df_index = getattr(row, 'Index')
                po = getattr(row, 'name')
                updated_at = getattr(row, 'updated_at')
                timestamp = time_ms(updated_at)
                cc_df.at[df_index, 'updated_at'] = timestamp
                created_at = getattr(row, 'created_at')
                cc_df.at[df_index, 'created_at'] = time_ms(created_at)
                id = getattr(row, 'id')
                if isinstance(id,str):
                    pass
                else:
                    id = create_id(po, timestamp, id_index)
                    cc_df.at[df_index, 'id'] = id
                id_index+=1

            local_user_sql = """select `id` as local_created_by ,crm_id as created_by from {}""".format("user_back")
            local_user_df = pd.read_sql_query(local_user_sql, new_data)
            cc_df = pd.merge(cc_df, local_user_df, how='left', on="created_by")
            cc_df = cc_df.drop(["created_by"], axis=1)
            cc_df = cc_df.rename(columns={"local_created_by": "created_by"})
            # updated_by
            local_user_df = local_user_df.rename(columns={"created_by": "updated_by"})
            cc_df = pd.merge(cc_df, local_user_df, how='left', on="updated_by")
            cc_df = cc_df.drop(["updated_by"], axis=1)
            cc_df = cc_df.rename(columns={"local_created_by": "updated_by"})

            cc_df = cc_df.drop_duplicates(["crm_id"], keep="first")
            print(cc_df)


            # 删除本次操作的所有local id
            delete_sql = """ delete from {} WHERE crm_id in ({}) """.format(self.sql_table,local_str)
            cur.execute(delete_sql)
            conn.commit()



            cur.close()
            conn.close()
            new_data.close()

            self.inster_sql(cc_df)





    def get_infos(self,p_index):
        list_index = p_index
        times = int(len(self.sql_index_list) /self.process_num) +2
        try:
            for i in range(times):
                print(self.sql_index_list[list_index])
                time.sleep(1)
                self.get_cloudcc_order(self.sql_index_list[list_index])
                list_index += 1
        except Exception as e:
            print(e)
            pass

    def merge_infos(self,nums,q,f_q):
        data_list=[]
        # 结束标志
        f_index = 0
        while True:
            # time.sleep(1)
            data_list_queue = q.get(True)
            data_list += data_list_queue
            print(len(data_list))
            if len(data_list) == nums:
                break
            f_index += f_q.get(True)
            print("f_index",f_index)

    def process_data(self):
        try:
            self.access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
            self.binding = cloudcc_get_binding(self.access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
        except:
            print("获取binding失败,请检查配置")
            return False
        try:
            count_sql = """  select count(*) as nums from {} """.format(self.cloudcc_object)
            count_data = cloudcc_query_sql(self.access_url, "cqlQuery", self.cloudcc_object, count_sql, self.binding)
            nums = count_data[0].get("nums",0)
        except:
            print("获取总数目失败")
            return False
        if nums % self.one_times_num > 0:
            num_times = int(nums / self.one_times_num) + 1
        elif nums % self.one_times_num == 0:
            num_times = int(nums / self.one_times_num)
        else:
            num_times = 0

        for index in range(num_times):
            if num_times == 1:
                index = 0
            start = int(index) * self.one_times_num
            if index == 0:
                start = 1
            self.sql_index_list.append(start)

        print(self.sql_index_list)
        self.sql_index_list = self.sql_index_list[::-1]
        p_l = []
        # Process(target=self.merge_infos, args=(nums,)).start()

        for i in range(self.process_num):
            p1 = Process(target=self.get_infos,args=(i,))
            p1.start()
            p_l.append(p1)
        for p in p_l:
            p.join()


if __name__ == "__main__":
    o = Order_Data()

    o.process_data()
    # o.get_cloudcc_order(0)












