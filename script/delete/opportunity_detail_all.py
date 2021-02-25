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

import numpy as np
import pymysql

import time
from datetime import datetime
import pandas as pd

from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.utils import engine, list_to_sql_string
from script.data_config import ORDER_DICT, ACCOUNT_DICT, OPPORTUNITY_DICT, OPPORTUNITY_TABLE_STRING, \
    OPPORTUNITY_DETAIL_DICT, OPPORTUNITY_DETAIL_TABLE_STRING
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

        # self.new_data = engine(settings.db_new_data)
        self.access_url  = ''
        self.binding = ''
        self.cloudcc_object="sjmx"
        self.sql_table= "opportunity_detail"
        self.sql_mapping= OPPORTUNITY_DETAIL_DICT

        self.one_times_num = 1000
        self.sql_index_list=[]

        # self.columns_order = ["id","crm_id","po","entity_type","ownerid","status","account_id","priceid","opportunity_id","created_by","created_at","updated_by","updated_at","amount","discount_amount","contract_status","contract_attribute","contractid","contract_start","contract_end","contract_back_date","total_performance","salerA","salerB","salerC","salerA_amount","salerB_amount","salerC_amount","approve_date","payback_type"]
        # self.ignore_key_list=["id","crm_id"]
        # self.df_list=[]






    def time_ms(self,date):
        try:
            if date:
                datetime_obj = datetime.strptime(date, "%Y-%m-%d %H:%M")
                obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
                obj_stamp = str(obj_stamp)
            else:
                obj_stamp = ""
            return obj_stamp
        except:
            # print(date,type(date))
            return ""

    def ms_date(self,ms_time):
        ms_time = int(ms_time)
        time_local = time.localtime(ms_time / 1000)
        date = time.strftime("%Y%m%d", time_local)
        return date[2:]

    def create_id(self,item_name,create_timestamp,index):
        md5_str = hashlib.md5(item_name.encode(encoding='UTF-8')+create_timestamp.encode(encoding='UTF-8')).hexdigest()[8:-8]
        md5_str = md5_str + index
        md5_str = self.id_per+md5_str
        return md5_str

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
        sql_remarks = OPPORTUNITY_DETAIL_TABLE_STRING.format(self.sql_table)
        cur.execute(sql_remarks)

        cur.close()
        conn.close()

        new_data.close()

    def get_cloudcc_order(self,index):

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
        sql_string = """ select {} from {} limit {},{} """
        sql = sql_string.format("*", self.cloudcc_object,index,self.one_times_num)
        # for i in range(3):
        data = cloudcc_query_sql(self.access_url, "cqlQuery",self.cloudcc_object, sql, self.binding)
        print("cc数据",len(data))
        #     if len(data) == self.one_times_num:
        #         print("获取",len(data))
        #         break
        #     else:
        #         print("重试{}".format(i),len(data))
        #         continue
        cc_df = pd.DataFrame(data)
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

        merge_local_df = local_df[["id","crm_id"]]
        cc_df = pd.merge(cc_df, merge_local_df, how='left', on="crm_id")
        cc_df = cc_df.drop(["is_deleted"],axis=1)




        # # 并集去重 取出差集
        # add_df = cc_df.append(local_df,sort=False)
        # add_df = add_df.drop_duplicates(subset=['crm_id'], keep=False)
        #
        # #add_df 新增   添加到local
        # local_df = local_df.append(add_df,sort=False)

        # 修改操作

        # 删除本次操作的所有local id
        delete_sql = """ delete from {} WHERE crm_id in ({}) """.format(self.sql_table,local_str)
        cur.execute(delete_sql)
        conn.commit()

        cur.close()
        conn.close()
        new_data.close()

        # time.sleep(random.randint(0,5))
        self.inster_sql(cc_df)









    def get_infos(self,p_index):
        list_index = p_index
        times = int(len(self.sql_index_list) /1) +2
        try:
            for i in range(times):
                print(self.sql_index_list[list_index])
                time.sleep(1)
                self.get_cloudcc_order(self.sql_index_list[list_index])
                list_index += 1
        except Exception as e:
            print(e)
            pass


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
            # nums = 500
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
                index = 1
            start = int(index) * self.one_times_num
            if index == 0:
                start = 1
            self.sql_index_list.append(start)

        print(self.sql_index_list)
        self.sql_index_list = self.sql_index_list[::-1]
        p_l = []
        # Process(target=self.merge_infos, args=(nums,)).start()

        for i in range(1):
            time.sleep(1)
            p1 = Process(target=self.get_infos,args=(i,))
            p1.start()
            p_l.append(p1)
        for p in p_l:
            p.join()


if __name__ == "__main__":
    o = Order_Data()

    # df = o.get_crm_data()
    # # print(order_df)
    # o.inster_sql(df)
    # o.close_connent()

    # o.get_cloudcc_order()

    o.process_data()
    # o.get_cloudcc_order(100)












