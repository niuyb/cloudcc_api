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


from multiprocessing import Process

import pymysql

import time
from datetime import datetime
import pandas as pd

from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.utils import engine, list_to_sql_string, time_ms
from script.data_config import ORDER_DICT, ORDER_TABLE_STRING,ORDER_SQL_TABLE, ORDER_API_NAME
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

        self.cloudcc_object=ORDER_API_NAME
        self.sql_table= ORDER_SQL_TABLE
        self.sql_mapping= ORDER_DICT
        self.sql_table_string = ORDER_TABLE_STRING

        self.access_url  = ''
        self.binding = ''
        self.today = datetime.now().strftime('%Y-%m-%d')
        print(self.today)
        # self.today = "2021-01-03"
        # 单次更新数量
        self.one_times_num = 1000
        self.sql_index_list=[]
        # 进程数目
        self.process_num = 1


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

    def inster_sql(self, df,local_str):
        new_data = engine(settings.db_new_data)
        cur, conn = self.get_conn()
        try:
            # 删除本次操作的所有local id
            delete_sql = """ delete from {} WHERE crm_id in ({}) """.format(self.sql_table, local_str)
            cur.execute(delete_sql)
            conn.commit()
            # 入库操作
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

    def get_cloudcc_infos(self,index):

        # self.today = "2020-12-29"
        new_data = engine(settings.db_new_data)

        if index == 1:
            index = 0
        # try:
        sql_string = """ select {} from {} where lastmodifydate like "%{}%" limit {},{} """
        sql = sql_string.format("*", self.cloudcc_object,self.today,index,self.one_times_num)
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

            # 在这里记录修改


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
            index_sql = """ select count(*) as nums from %s where created_at like "%s" """%(self.sql_table,self.today)
            id_index = pd.read_sql_query(index_sql,new_data)["nums"].tolist()[0]
            print(id_index)
            for row in cc_df.itertuples():
                df_index = getattr(row, 'Index')
                po = getattr(row, 'po')
                created_at = getattr(row, 'created_at')
                timestamp = time_ms(created_at)
                id = getattr(row, 'id')
                if isinstance(id,str):
                    pass
                else:
                    id = create_id(po, timestamp, id_index)
                    print(id)
                    cc_df.at[df_index, 'id'] = id
                id_index+=1

            new_data.close()

            self.inster_sql(cc_df,local_str)

    def get_infos(self,p_index):
        list_index = p_index
        times = int(len(self.sql_index_list) /self.process_num) +2
        try:
            for i in range(times):
                print(self.sql_index_list[list_index])
                time.sleep(1)
                self.get_cloudcc_infos(self.sql_index_list[list_index])
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
                index = 1
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
    # o.get_cloudcc_infos(0)












