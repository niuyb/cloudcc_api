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
path1 = os.path.abspath('/var/www/cloudcc_api')
sys.path.append(path1)

from multiprocessing import Process

import pymysql

import pandas as pd

from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.utils import engine, list_to_sql_string, time_ms, date_ms
from script.data_config import  USER_SQL_TABLE, \
    ACCOUNT_SQL_TABLE, ACCOUNT_API_NAME, ACCOUNT_DICT, ACCOUNT_TABLE_STRING, ACCOUNT_CLOUMNS_ORDER
from script.data_utils import create_id
from settings import settings
from settings.config import ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD

pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)# 展示所有列


"""
price_id  暂时未转换

"""


class Order_Data():
    def __init__(self):

        self.access_url  = ''
        self.binding = ''
        self.cloudcc_object=ACCOUNT_API_NAME
        self.sql_table= ACCOUNT_SQL_TABLE
        # self.sql_table= "account_back_copy1"
        self.sql_mapping= ACCOUNT_DICT
        self.sql_table_string = ACCOUNT_TABLE_STRING
        self.user_table = USER_SQL_TABLE
        # self.account_table = ACCOUNT_SQL_TABLE
        # self.account_table = "account_back_copy"


        # self.today = str(datetime.now().strftime('%Y-%m-%d'))
        self.today = (datetime.datetime.now() - datetime.timedelta(hours=1.5)).strftime('%Y-%m-%d')

        # self.today_stamp =  date_ms(self.today)
        # self.today = "2021-01-06"
        print(self.today)
        self.one_times_num = 1000
        self.sql_index_list=[]
        self.process_num = 1
        self.columns_order = ACCOUNT_CLOUMNS_ORDER


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

    def inster_sql(self, df,local_str):

        new_data = engine(settings.db_new_data)
        cur, conn = self.get_conn()
        try:
            # 删除本次操作的所有local id
            delete_sql = """ delete from {} WHERE crm_id in ({}) """.format(self.sql_table, local_str)
            cur.execute(delete_sql)
            conn.commit()
            # 入库操作
            df = df[self.columns_order]
            df.to_sql(self.sql_table, new_data, index=False, if_exists="append")
            # 修改类型
            sql_remarks = self.sql_table_string.format(self.sql_table)
            cur.execute(sql_remarks)
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()
            new_data.close()

    def get_repeat_order(self,index):
        if index == 1:
            index = 0
        new_data = engine(settings.db_new_data)
        # try:
        sql_string = """ select crm_id from account_back """
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

    def get_cloudcc_order(self,index):

        new_data = engine(settings.db_new_data)


        sql_string = """ select crm_id from account_back """
        cc_df = pd.read_sql_query(sql_string,new_data)
        print(cc_df.shape)
        delete_df = cc_df.drop_duplicates(keep=False)
        print(delete_df.shape)

        keep_df = cc_df.drop_duplicates(keep="first")
        print(keep_df.shape)

        id_df=delete_df.append(keep_df).drop_duplicates(keep=False)
        print(id_df.shape)

        new_data.close()



    def get_infos(self,p_index):
        list_index = p_index
        times = int(len(self.sql_index_list) /self.process_num) +2
        try:
            for i in range(times):
                print(self.sql_index_list[list_index])
                self.get_cloudcc_order(self.sql_index_list[list_index])
                list_index += 1
        except Exception as e:
            print("get_infos------",e)
            pass

    def process_data(self):
        try:
            self.access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
            self.binding = cloudcc_get_binding(self.access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
        except:
            print("获取binding失败,请检查配置")
            return False
        try:
            count_sql = """  select count(*) as nums from %s where left(lastmodifydate,10) = '%s' """%(self.cloudcc_object,self.today)
            print(count_sql)
            count_data = cloudcc_query_sql(self.access_url, "cqlQuery", self.cloudcc_object, count_sql, self.binding)
            nums = count_data[0].get("nums",0)
            print(count_data)
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
            start = int(index) * self.one_times_num
            if num_times == 1:
                start = 1
            if index == 0:
                start = 1
            self.sql_index_list.append(start)

        print(self.sql_index_list)
        self.sql_index_list = self.sql_index_list[::-1]

        p_l = []
        for i in range(self.process_num):
            p1 = Process(target=self.get_infos,args=(i,))
            p1.start()
            p_l.append(p1)
        for p in p_l:
            p.join()


if __name__ == "__main__":
    o = Order_Data()

    # o.process_data()
    o.get_repeat_order(0)












